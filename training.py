#----------------------------------------------------------------------------------------------------------------------------------------
# LIBRARIES
import argparse
import torch
import pandas as pd
from models import VAE,vae_loss,kaiming_weights_init
from tqdm import trange
#----------------------------------------------------------------------------------------------------------------------------------------
# GLOBAL (DEFAULT) PARAMETERS AND SETTINGS
torch.manual_seed(1610); # Reproducibility seed

DATA_PATH        = 'data/training_dataset.csv'
CHECKPOINTS_PATH = 'checkpoints/vae.pth'
HIDDEN_DIM1      = 64
HIDDEN_DIM2      = 32
LATENT_DIM       = 16  
LR               = 1e-2
BATCH_SIZE       = 512 
EPOCHS           = 1200
DEVICE           = 'cuda' if torch.cuda.is_available() else 'mps' if torch.backends.mps.is_available() else 'cpu'
WARMUP           = False



if __name__ == "__main__":
    
    #----------------------------------------------------------------------------------------------------------------------------------------
    # PARSE ARGUMENTS 
    parser = argparse.ArgumentParser(
        description = "Python script to train a Variational Autoencoder (VAE) on football player data"
        )
 
    # Paths
    parser.add_argument("-DP","--DataPath",
                        type    = str,
                        default = DATA_PATH,
                        help    = "Path to the training dataset"
                       )
    parser.add_argument("-CP","--CheckpointsPath",
                        type    = str,
                        default = CHECKPOINTS_PATH,
                        help    = "Path to the model checkpoints"
                       )
    
    # Hyperparameters
    parser.add_argument("-H1","--HiddenDim1",
                        type    = int,
                        default = HIDDEN_DIM1,
                        help    = "Hidden dimension 1"
                       )
    parser.add_argument("-H2","--HiddenDim2",
                        type    = int,
                        default = HIDDEN_DIM2,
                        help    = "Hidden dimension 2"
                       )
    parser.add_argument("-LD","--LatentDim",
                        type    = int,
                        default = LATENT_DIM,
                        help    = "Latent dimension"
                       )
    parser.add_argument("-LR","--LearningRate",
                        type    = float,
                        default = LR,
                        help    = "Learning rate"
                       )
    parser.add_argument("-BS","--BatchSize",
                        type    = int,
                        default = BATCH_SIZE,
                        help    = "Batch size"
                       )
    parser.add_argument("-E","--Epochs",
                        type    = int,
                        default = EPOCHS,
                        help    = "Number of epochs"
                       )
    
    # Other settings
    parser.add_argument("-W","--Warmup", 
                        action  = "store_true",
                        help    = "Add this flag to enable warmup settings for the beta parameter"
                       )
    

    args = parser.parse_args()
    
    #----------------------------------------------------------------------------------------------------------------------------------------
    # DATA IMPORT AND PREPROCESSING
    
    data = pd.read_csv(args.DataPath)
    # Drop non-numeric columns and normalize data
    X = data.drop(['Player', 'Nation', 'Pos_fbref','Pos_tm', 'Squad','League', 'Born','90s','MarketValue'], axis=1).to_numpy(dtype='float32')
    X = torch.tensor(X, dtype=torch.float32)
    X = (X -X.mean(dim=0)) / X.std(dim=0)

    # Train-test split
    #train_idx = torch.randperm(X.shape[0])[:int(0.8*X.shape[0])]
    #X_train   = X[train_idx]
    #X_test    = X[~train_idx]
    permuted_idx = torch.randperm(X.shape[0])
    X_train   = X[permuted_idx[:int(0.8*X.shape[0])]]
    X_test    = X[permuted_idx[int(0.8*X.shape[0]):]]
    train_loader = torch.utils.data.DataLoader(X_train, batch_size = args.BatchSize, shuffle = True)
    test_loader  = torch.utils.data.DataLoader(X_test , batch_size = args.BatchSize, shuffle = False)

    #----------------------------------------------------------------------------------------------------------------------------------------
    # MODEL TRAINING

    vae = VAE(
        input_dim   = X.shape[1],
        latent_dim  = args.LatentDim,
        hidden_dim1 = args.HiddenDim1,
        hidden_dim2 = args.HiddenDim2).to(DEVICE)

    vae.apply(kaiming_weights_init)

    optimizer = torch.optim.AdamW(vae.parameters(), lr=args.LearningRate,weight_decay=0.001,betas=(0.9, 0.99))
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, 'min', factor=0.75, patience=50,min_lr = 1e-6)

    if args.Warmup:
        warmup_epochs =  args.Epochs // 10
        betas = torch.linspace(0, 1, warmup_epochs)
        betas = torch.cat((betas,torch.ones(args.Epochs - warmup_epochs))).to(DEVICE)
    else:
        betas = torch.full((args.Epochs,),1.0).to(DEVICE)
        

    losses = []
    r_losses = []
    kl_losses = []
    test_losses = []

    tqdm_bar = trange(args.Epochs,desc='Training')

    for epoch in tqdm_bar:
        # Training
        vae.train()
        total_loss = 0
        total_kl_loss = 0
        total_r_loss = 0
        for batch in train_loader:  
            batch = batch.to(DEVICE)
            optimizer.zero_grad()
            
            reconstructed, mu, logvar = vae(batch)
            loss,r_loss,kl_loss = vae_loss(reconstructed, batch, mu, logvar, betas[epoch])
            loss.backward()
            #torch.nn.utils.clip_grad_norm_(vae.parameters(),2)
            optimizer.step()
            
            total_loss += loss.item()
            total_kl_loss += kl_loss.item()
            total_r_loss += r_loss.item()
            
            
        losses += [total_loss / len(train_loader)]
        r_losses += [total_r_loss / len(train_loader)]
        kl_losses += [total_kl_loss / len(train_loader)]
        
        # Evaluation
        vae.eval()
        total_test_loss = 0
        for test_batch in test_loader:  
            test_batch = test_batch.to(DEVICE)
            
            test_reconstructed, test_mu, test_logvar = vae(test_batch)
            test_loss,_,_ = vae_loss(test_reconstructed, test_batch, test_mu, test_logvar, betas[epoch])
            
            total_test_loss += test_loss.item()
        test_losses += [total_test_loss / len(test_loader)]
        
        scheduler.step(test_losses[-1])
        
        tqdm_bar.set_description(
        f"Epoch {epoch + 1} | "
        f"Train Loss: {total_loss / len(train_loader):.4f} | "
        f"Test Loss: {total_test_loss / len(test_loader):.4f} | "
        f"LR: {optimizer.param_groups[0]['lr']:.4f}"
        )
        
        torch.save(vae.state_dict(), args.CheckpointsPath)

    #----------------------------------------------------------------------------------------------------------------------------------------