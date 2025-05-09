
# check pytorch check cuda

import torch


def check_cuda():
    """
    Check if CUDA is available and print the CUDA version.
    """
    if torch.cuda.is_available():
        print("CUDA is available.")
        print(f"CUDA version: {torch.version.cuda}")
    else:
        print("CUDA is not available.")
        print("Please check your CUDA installation.")

if __name__ == "__main__":
    check_cuda()
