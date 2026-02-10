from create_generator_model import GAN

if __name__ == "__main__":
    gan = GAN(batch_size=24)
    gan.train()

    # Save the generator and discriminator models
    # gan.generator.save("generator_model.h5")
    # gan.discriminator.save("discriminator_model.h5")
