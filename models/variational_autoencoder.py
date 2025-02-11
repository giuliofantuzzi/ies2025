import torch

# VAE class
class VAE(torch.nn.Module):
    def __init__(self, input_dim, hidden_dim1, hidden_dim2, latent_dim, leaky_relu_alpha=None):
        super(VAE, self).__init__()
        
        # Encoder
        self.encoder = torch.nn.Sequential(
            torch.nn.Linear(input_dim, hidden_dim1),
            torch.nn.ReLU() if leaky_relu_alpha is None else torch.nn.LeakyReLU(leaky_relu_alpha),
            torch.nn.Linear(hidden_dim1, hidden_dim2),
            torch.nn.ReLU() if leaky_relu_alpha is None else torch.nn.LeakyReLU(leaky_relu_alpha),
        )
        
        # Latent space
        self.mu_layer = torch.nn.Linear(hidden_dim2, latent_dim)        
        self.logvar_layer = torch.nn.Linear(hidden_dim2, latent_dim)    
        
        # Decoder
        self.decoder = torch.nn.Sequential(
            torch.nn.Linear(latent_dim, hidden_dim2),
            torch.nn.ReLU() if leaky_relu_alpha is None else torch.nn.LeakyReLU(leaky_relu_alpha),
            torch.nn.Linear(hidden_dim2, hidden_dim1),
            torch.nn.ReLU() if leaky_relu_alpha is None else torch.nn.LeakyReLU(leaky_relu_alpha),
            torch.nn.Linear(hidden_dim1, input_dim)
        )
    
    def encode(self, x):
        """Encodes input into latent mean and log-variance."""
        h = self.encoder(x)
        mu = self.mu_layer(h)
        logvar = self.logvar_layer(h)
        return mu, logvar

    def reparameterize(self, mu, logvar):
        """Reparameterization trick to sample z from the latent distribution."""
        std = torch.exp(0.5 * logvar)  # Standard deviation
        eps = torch.randn_like(std)  # Random noise
        return mu + eps * std  # Reparameterized sample

    def decode(self, z):
        """Decodes latent vector into reconstructed input."""
        return self.decoder(z)
    
    def forward(self, x):
        """Forward pass through the VAE."""
        mu, logvar = self.encode(x)
        z = self.reparameterize(mu, logvar)
        x_reconstructed = self.decode(z)
        return x_reconstructed, mu, logvar
 
 
# VAE loss function (beta-VAE generalized version)
def vae_loss(reconstructed, original, mu, logvar,beta=1.0):
    """Computes the VAE loss: reconstruction loss + KL divergence."""
    
    # Reconstruction loss (binary cross-entropy)
    reconstruction_loss = torch.nn.functional.mse_loss(reconstructed, original, reduction='sum')
    # KL divergence
    kl_divergence = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
    # Total loss 
    loss = reconstruction_loss + beta*kl_divergence
    
    return loss, reconstruction_loss, kl_divergence
    

def kaiming_weights_init(m):
    if isinstance(m, torch.nn.Linear) or isinstance(m, torch.nn.Conv2d) or isinstance(m, torch.nn.ConvTranspose2d):
        torch.nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')  # Kaiming for ReLU
        if m.bias is not None:
            torch.nn.init.zeros_(m.bias) 