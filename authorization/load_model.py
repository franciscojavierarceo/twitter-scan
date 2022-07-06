import os
import torch
import transformers

MODEL_URLS = {
    "original-small": "./original-albert-0e1d6498.ckpt",
}

PRETRAINED_MODEL = None


def get_model_and_tokenizer(
    model_type,
    model_name,
    tokenizer_name,
    num_classes,
    state_dict,
    huggingface_config_path=None,
):
    model_class = getattr(transformers, model_name)
    model = model_class.from_pretrained(
        pretrained_model_name_or_path=None,
        config=huggingface_config_path or model_type,
        num_labels=num_classes,
        state_dict=state_dict,
        local_files_only=huggingface_config_path is not None,
    )
    tokenizer = getattr(transformers, tokenizer_name).from_pretrained(
        huggingface_config_path or model_type,
        local_files_only=huggingface_config_path is not None,
        # TODO: may be needed to let it work with Kaggle competition
        # model_max_length=512,
    )

    return model, tokenizer


def load_checkpoint(
    model_type="original-small",
    checkpoint=None,
    device="cpu",
    huggingface_config_path=None,
):
    print("loading model...")
    if checkpoint is None:
        checkpoint_path = MODEL_URLS[model_type]
        # loaded = torch.hub.load_state_dict_from_url(checkpoint_path, map_location=device)
        loaded = torch.load(checkpoint_path, map_location=device)
    else:
        loaded = torch.load(checkpoint, map_location=device)
        if "config" not in loaded or "state_dict" not in loaded:
            raise ValueError(
                "Checkpoint needs to contain the config it was trained \
                    with as well as the state dict"
            )
    class_names = loaded["config"]["dataset"]["args"]["classes"]
    # standardise class names between models
    change_names = {
        "toxic": "toxicity",
        "identity_hate": "identity_attack",
        "severe_toxic": "severe_toxicity",
    }
    class_names = [change_names.get(cl, cl) for cl in class_names]
    model, tokenizer = get_model_and_tokenizer(
        **loaded["config"]["arch"]["args"],
        state_dict=loaded["state_dict"],
        huggingface_config_path=huggingface_config_path,
    )

    return model, tokenizer, class_names


def load_model(model_type, checkpoint=None):
    if checkpoint is None:
        model, _, _ = load_checkpoint(model_type=model_type)
    else:
        model, _, _ = load_checkpoint(checkpoint=checkpoint)
    return model


class Detoxify:
    """Detoxify
    Easily predict if a comment or list of comments is toxic.
    Can initialize 5 different model types from model type or checkpoint path:
        - original:
            model trained on data from the Jigsaw Toxic Comment
            Classification Challenge
        - unbiased:
            model trained on data from the Jigsaw Unintended Bias in
            Toxicity Classification Challenge
        - multilingual:
            model trained on data from the Jigsaw Multilingual
            Toxic Comment Classification Challenge
        - original-small:
            lightweight version of the original model
        - unbiased-small:
            lightweight version of the unbiased model
    Args:
        model_type(str): model type to be loaded, can be either original,
                         unbiased or multilingual
        checkpoint(str): checkpoint path, defaults to None
        device(str or torch.device): accepts any torch.device input or
                                     torch.device object, defaults to cpu
        huggingface_config_path: path to HF config and tokenizer files needed for offline model loading
    Returns:
        results(dict): dictionary of output scores for each class
    """

    def __init__(
        self,
        model_type="original-small",
        checkpoint=PRETRAINED_MODEL,
        device="cpu",
        huggingface_config_path=None,
    ):
        super().__init__()
        self.model, self.tokenizer, self.class_names = load_checkpoint(
            model_type=model_type,
            checkpoint=checkpoint,
            device=device,
            huggingface_config_path=huggingface_config_path,
        )
        self.device = device
        self.model.to(self.device)

    @torch.no_grad()
    def predict(self, text):
        self.model.eval()
        inputs = self.tokenizer(
            text, return_tensors="pt", truncation=True, padding=True
        ).to(self.model.device)
        out = self.model(**inputs)[0]
        scores = torch.sigmoid(out).cpu().detach().numpy()
        results = {}
        for i, cla in enumerate(self.class_names):
            results[cla] = (
                scores[0][i]
                if isinstance(text, str)
                else [scores[ex_i][i].tolist() for ex_i in range(len(scores))]
            )
        return results


def toxic_albert():
    return load_model("original-small")


def main():
    m = Detoxify("original-small")
    print(m.predict("this is a test"))


if __name__ == "__main__":
    main()
