import argparse
from koBERT.predict import predict

def define_argparser():
    p = argparse.ArgumentParser()

    p.add_argument('--gpu_id', type=int, default=0)
    p.add_argument('--dropout_p', type=float, default=.5)
    p.add_argument('--learning_rate', type=float, default=5e-5)
    p.add_argument('--warmup_ratio', type=float, default=0.1)
    p.add_argument('--max_len', type=int, default=64)
    p.add_argument('--num_epochs', type=int, default=5)
    p.add_argument('--max_grad_norm', type=int, default=1)
    p.add_argument('--log_interval', type=int, default=200)

    config = p.parse_args()
    return config


if __name__ == '__main__':
    config = define_argparser()
    for i in range(5):
        text = input("확인할 리뷰를 입력하세요\n")
        result = predict(config, text)
        
        if result == 1:
            print("보통이에요")
        
        elif result == 2:
            print("좋아요")
        
        else:
            print("별로에요")