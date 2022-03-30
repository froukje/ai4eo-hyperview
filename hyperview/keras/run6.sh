#!/bin/bash -x

srun -N1 -p booster --account=hai_cons_ee --gres gpu:4 --time=15:00:00 --pty singularity exec --bind "${PWD}:/mnt" --nv ../hyperview_latest.sif python main.py -m 0 -c 6 -l 0.1000 -b 16 -w 224  --num-epochs 89 -p --train-dir 'train_data/train_data/' --label-dir 'train_data/train_gt.csv' --eval-dir 'test_data/' --out-dir 'modeldir/' &
srun -N1 -p booster --account=hai_cons_ee --gres gpu:4 --time=15:00:00 --pty singularity exec --bind "${PWD}:/mnt" --nv ../hyperview_latest.sif python main.py -m 0 -c 6 -l 0.0100 -b 16 -w 224  --num-epochs 89 -p --train-dir 'train_data/train_data/' --label-dir 'train_data/train_gt.csv' --eval-dir 'test_data/' --out-dir 'modeldir/' &
srun -N1 -p booster --account=hai_cons_ee --gres gpu:4 --time=15:00:00 --pty singularity exec --bind "${PWD}:/mnt" --nv ../hyperview_latest.sif python main.py -m 0 -c 6 -l 0.0010 -b 16 -w 224  --num-epochs 89 -p --train-dir 'train_data/train_data/' --label-dir 'train_data/train_gt.csv' --eval-dir 'test_data/' --out-dir 'modeldir/' &
srun -N1 -p booster --account=hai_cons_ee --gres gpu:4 --time=15:00:00 --pty singularity exec --bind "${PWD}:/mnt" --nv ../hyperview_latest.sif python main.py -m 0 -c 6 -l 0.0001 -b 16 -w 224  --num-epochs 89 -p --train-dir 'train_data/train_data/' --label-dir 'train_data/train_gt.csv' --eval-dir 'test_data/' --out-dir 'modeldir/' &
srun -N1 -p booster --account=hai_cons_ee --gres gpu:4 --time=15:00:00 --pty singularity exec --bind "${PWD}:/mnt" --nv ../hyperview_latest.sif python main.py -m 1 -c 6 -l 0.1000 -b 16 -w 224  --num-epochs 89 -p --train-dir 'train_data/train_data/' --label-dir 'train_data/train_gt.csv' --eval-dir 'test_data/' --out-dir 'modeldir/' &
srun -N1 -p booster --account=hai_cons_ee --gres gpu:4 --time=15:00:00 --pty singularity exec --bind "${PWD}:/mnt" --nv ../hyperview_latest.sif python main.py -m 1 -c 6 -l 0.0100 -b 16 -w 224  --num-epochs 89 -p --train-dir 'train_data/train_data/' --label-dir 'train_data/train_gt.csv' --eval-dir 'test_data/' --out-dir 'modeldir/' &
srun -N1 -p booster --account=hai_cons_ee --gres gpu:4 --time=15:00:00 --pty singularity exec --bind "${PWD}:/mnt" --nv ../hyperview_latest.sif python main.py -m 1 -c 6 -l 0.0010 -b 16 -w 224  --num-epochs 89 -p --train-dir 'train_data/train_data/' --label-dir 'train_data/train_gt.csv' --eval-dir 'test_data/' --out-dir 'modeldir/' &
srun -N1 -p booster --account=hai_cons_ee --gres gpu:4 --time=15:00:00 --pty singularity exec --bind "${PWD}:/mnt" --nv ../hyperview_latest.sif python main.py -m 1 -c 6 -l 0.0001 -b 16 -w 224  --num-epochs 89 -p --train-dir 'train_data/train_data/' --label-dir 'train_data/train_gt.csv' --eval-dir 'test_data/' --out-dir 'modeldir/' &
srun -N1 -p booster --account=hai_cons_ee --gres gpu:4 --time=15:00:00 --pty singularity exec --bind "${PWD}:/mnt" --nv ../hyperview_latest.sif python main.py -m 2 -c 6 -l 0.1000 -b 16 -w 224  --num-epochs 89 -p --train-dir 'train_data/train_data/' --label-dir 'train_data/train_gt.csv' --eval-dir 'test_data/' --out-dir 'modeldir/' &
srun -N1 -p booster --account=hai_cons_ee --gres gpu:4 --time=15:00:00 --pty singularity exec --bind "${PWD}:/mnt" --nv ../hyperview_latest.sif python main.py -m 2 -c 6 -l 0.0100 -b 16 -w 224  --num-epochs 89 -p --train-dir 'train_data/train_data/' --label-dir 'train_data/train_gt.csv' --eval-dir 'test_data/' --out-dir 'modeldir/' &
srun -N1 -p booster --account=hai_cons_ee --gres gpu:4 --time=15:00:00 --pty singularity exec --bind "${PWD}:/mnt" --nv ../hyperview_latest.sif python main.py -m 2 -c 6 -l 0.0010 -b 16 -w 224  --num-epochs 89 -p --train-dir 'train_data/train_data/' --label-dir 'train_data/train_gt.csv' --eval-dir 'test_data/' --out-dir 'modeldir/' &
srun -N1 -p booster --account=hai_cons_ee --gres gpu:4 --time=15:00:00 --pty singularity exec --bind "${PWD}:/mnt" --nv ../hyperview_latest.sif python main.py -m 2 -c 6 -l 0.0001 -b 16 -w 224  --num-epochs 89 -p --train-dir 'train_data/train_data/' --label-dir 'train_data/train_gt.csv' --eval-dir 'test_data/' --out-dir 'modeldir/' &
srun -N1 -p booster --account=hai_cons_ee --gres gpu:4 --time=15:00:00 --pty singularity exec --bind "${PWD}:/mnt" --nv ../hyperview_latest.sif python main.py -m 3 -c 6 -l 0.1000 -b 16 -w 224  --num-epochs 89 -p --train-dir 'train_data/train_data/' --label-dir 'train_data/train_gt.csv' --eval-dir 'test_data/' --out-dir 'modeldir/' &
srun -N1 -p booster --account=hai_cons_ee --gres gpu:4 --time=15:00:00 --pty singularity exec --bind "${PWD}:/mnt" --nv ../hyperview_latest.sif python main.py -m 3 -c 6 -l 0.0100 -b 16 -w 224  --num-epochs 89 -p --train-dir 'train_data/train_data/' --label-dir 'train_data/train_gt.csv' --eval-dir 'test_data/' --out-dir 'modeldir/' &
srun -N1 -p booster --account=hai_cons_ee --gres gpu:4 --time=15:00:00 --pty singularity exec --bind "${PWD}:/mnt" --nv ../hyperview_latest.sif python main.py -m 3 -c 6 -l 0.0010 -b 16 -w 224  --num-epochs 89 -p --train-dir 'train_data/train_data/' --label-dir 'train_data/train_gt.csv' --eval-dir 'test_data/' --out-dir 'modeldir/' &
srun -N1 -p booster --account=hai_cons_ee --gres gpu:4 --time=15:00:00 --pty singularity exec --bind "${PWD}:/mnt" --nv ../hyperview_latest.sif python main.py -m 3 -c 6 -l 0.0001 -b 16 -w 224  --num-epochs 89 -p --train-dir 'train_data/train_data/' --label-dir 'train_data/train_gt.csv' --eval-dir 'test_data/' --out-dir 'modeldir/' &
