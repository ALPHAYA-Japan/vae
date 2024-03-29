'''
    ------------------------------------
    Author : SAHLI Mohammed
    Date   : 2019-11-11
    Company: Alphaya (www.alphaya.com)
    Email  : nihon.sahli@gmail.com
    ------------------------------------
'''

import sys
from src.VAE  import VAE
from src.CVAE import CVAE
from src.infoVAE import infoVAE
from src.MMDVAE import MMDVAE

# --------------------------------------Main-----------------------------------------
if __name__ == "__main__":
    models = {"VAE"     : VAE,
              "CVAE"    : CVAE,
              "infoVAE" : infoVAE,
              "MMDVAE"  : MMDVAE}

    # ...........................................
    if len(sys.argv) < 3:
        print("command 1: python train.py VAE_type train")
        print("command 2: python train.py VAE_type generate")
        print("command 3: python train.py VAE_type generate path/to/image")
        print("VAE_type can be",[a for a in models.keys()])
        sys.exit()

    model = sys.argv[1] #.upper()
    mode  = sys.argv[2]

    if model not in models:
        print(model,"not in",[a for a in models.keys()])
        sys.exit()
    elif mode not in ["train", "generate"]:
        print(mode,"not in",["train","generate"])
        sys.exit()

    # ...........................................
    data_path   = 'data/MNIST/train_data/'          # training data location (see README)
    model_path  = 'models/'+model+'_MNIST/'         # specify where you wanna save your model

    # ...........................................
    image_size = 32
    if mode == "train":
        vae = models[model](data_path  = data_path,
                            model_path = model_path,
                            is_training= True,     # Must be True for training
                            batch_size = 64,
                            image_size = image_size,
                            latent_dim = 200,
                            hard_load  = True,     # if True, load all images at once
                            pretrained = False,    # if True, load a pretrained model
                            verbose    = True)
        vae.train(max_epoches = 30,                # Maximum number of epochs
                  show_images = False)             # if True, you can see some generated images
                                                   # during training
    else:
        vae = models[model](model_path = model_path,
                            image_size = image_size)
        if len(sys.argv) == 3:
            vae.generate(source     = data_path,
                         samples    = 20,
                         grid_width = 480,
                         grid_height= 240,
                         destination= 'images/'+model+'/grid.png')
        elif len(sys.argv) == 4:
            vae = models[model](model_path = model_path,
                                image_size = image_size)
            vae.generate(source     = sys.argv[3],
                         destination= 'images/'+model+'/grid.png')
        else:
            print("command 1: python train.py VAE_type train")
            print("command 2: python train.py VAE_type generate")
            print("command 3: python train.py VAE_type generate path/to/image")
            print("VAE_type can be",[a for a in models.keys()])
            sys.exit()
