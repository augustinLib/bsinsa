import argparse
from koBERT.trainer import train


def define_argparser():
    p = argparse.ArgumentParser()

    p.add_argument("--model_name", required=True)
    p.add_argument("--gpu_id", type=int, default=0)
    p.add_argument("--batch_size", type=int, default=64)
    p.add_argument("--dropout_p", type=float, default=0.5)
    p.add_argument("--learning_rate", type=float, default=5e-5)
    p.add_argument("--warmup_ratio", type=float, default=0.1)
    p.add_argument("--max_len", type=int, default=64)
    p.add_argument("--num_epochs", type=int, default=5)
    p.add_argument("--max_grad_norm", type=int, default=1)
    p.add_argument("--log_interval", type=int, default=200)

    config = p.parse_args()
    return config


def main(config):
    train(config)


if __name__ == "__main__":
    config = define_argparser()
    main(config)