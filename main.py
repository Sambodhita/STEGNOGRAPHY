import click
import os
from src.steganography import LSBSteganography

@click.group()
def cli():
    """Advanced Steganography Tool"""
    pass

@cli.command()
@click.option('--image', '-i', required=True)
@click.option('--message', '-m', required=True)
@click.option('--password', '-p', required=True)
@click.option('--output', '-o', required=True)
def embed(image, message, password, output):
    """Hide message in image"""
    stego = LSBSteganography()
    success = stego.embed_message(image, message, password, output)
    if success:
        print(f"SUCCESS: Message hidden in {output}")
    else:
        print("FAILED to hide message")

@cli.command()
@click.option('--image', '-i', required=True)
@click.option('--password', '-p', required=True)
def extract(image, password):
    """Extract message from image"""
    stego = LSBSteganography()
    message = stego.extract_message(image, password)
    if message:
        print(f"EXTRACTED MESSAGE: {message}")
    else:
        print("NO MESSAGE FOUND")

if __name__ == '__main__':
    cli()
