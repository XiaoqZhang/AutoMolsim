import hydra
from omegaconf import DictConfig, OmegaConf
from raspa_molsim import running


commands = {
    "prep": running.run_preprocessing,
    "post": running.run_postprocessing
}

@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(cfg: DictConfig) -> None:
    commands[cfg.mode](cfg)
    
    
if __name__ == "__main__":
    main()