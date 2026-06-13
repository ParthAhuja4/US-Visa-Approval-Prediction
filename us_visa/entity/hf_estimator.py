import os
import sys
import joblib
from huggingface_hub import HfApi, hf_hub_download
from us_visa.exception import USvisaException
from us_visa.logger import logging
from dotenv import load_dotenv

load_dotenv()


class USvisaEstimator:
    """
    Handles saving/loading the trained model to/from Hugging Face Hub.
    Acts as a drop-in replacement for the S3-based estimator.
    """

    def __init__(self, repo_id: str, model_filename: str = "model.pkl"):
        """
        :param repo_id: HuggingFace repo, e.g. "your-username/usvisa-model"
        :param model_filename: filename inside the repo, e.g. "model.pkl"
        """
        self.repo_id = repo_id
        self.model_filename = model_filename
        self.api = HfApi()
        self.token = os.getenv("HUGGINGFACE_TOKEN")

    def is_model_present(self) -> bool:
        """Check if the model file exists in the HF repo."""
        try:
            files = self.api.list_repo_files(self.repo_id, token=self.token)
            return self.model_filename in list(files)
        except Exception:
            return False  # Repo doesn't exist yet or is empty

    def save_model(self, from_file: str) -> None:
        """Upload a local model file to the HF repo."""
        try:
            logging.info(f"Uploading model from {from_file} to HF repo: {self.repo_id}")

            # Create the repo if it doesn't exist yet
            self.api.create_repo(
                repo_id=self.repo_id,
                token=self.token,
                exist_ok=True,  # won't fail if repo already exists
                private=True,  # set False if you want a public repo
            )

            self.api.upload_file(
                path_or_fileobj=from_file,
                path_in_repo=self.model_filename,
                repo_id=self.repo_id,
                token=self.token,
            )
            logging.info("Model uploaded successfully to Hugging Face Hub.")
        except Exception as e:
            raise USvisaException(e, sys) from e

    def predict(self, x):
        """Download model from HF Hub and run prediction."""
        try:
            local_path = hf_hub_download(
                repo_id=self.repo_id,
                filename=self.model_filename,
                token=self.token,
            )
            model = joblib.load(local_path)
            return model.predict(x)
        except Exception as e:
            raise USvisaException(e, sys) from e
