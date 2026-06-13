import sys

from us_visa.exception import USvisaException
from us_visa.logger import logging
from us_visa.entity.artifact_entity import ModelPusherArtifact, ModelEvaluationArtifact
from us_visa.entity.config_entity import ModelPusherConfig
from us_visa.entity.hf_estimator import USvisaEstimator


class ModelPusher:
    def __init__(
        self,
        model_evaluation_artifact: ModelEvaluationArtifact,
        model_pusher_config: ModelPusherConfig,
    ):
        self.model_evaluation_artifact = model_evaluation_artifact
        self.model_pusher_config = model_pusher_config
        self.usvisa_estimator = USvisaEstimator(
            repo_id=model_pusher_config.hf_repo_id,
            model_filename=model_pusher_config.hf_model_filename,
        )

    def initiate_model_pusher(self) -> ModelPusherArtifact:
        logging.info("Entered initiate_model_pusher method of ModelPusher class")
        try:
            self.usvisa_estimator.save_model(
                from_file=self.model_evaluation_artifact.trained_model_path
            )
            model_pusher_artifact = ModelPusherArtifact(
                hf_repo_id=self.model_pusher_config.hf_repo_id,
                hf_model_path=self.model_pusher_config.hf_model_filename,
            )
            logging.info(f"Model pusher artifact: [{model_pusher_artifact}]")
            return model_pusher_artifact
        except Exception as e:
            raise USvisaException(e, sys) from e
