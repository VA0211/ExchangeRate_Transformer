export CUDA_VISIBLE_DEVICES=2

model_name=iTransformer

python -u run.py \
  --is_training 1 \
  --root_path D:/FPT/SU24/DSP391m/try/iTransformer/data/real/ \
  --data_path df_combine.csv \
  --model_id custom_model \
  --model $model_name \
  --data custom \
  --features MS \
  --target 'Sell' \
  --freq 'd' \
  --seq_len 60 \
  --pred_len 60 \
  --e_layers 1 \
  --enc_in 9 \
  --dec_in 9 \
  --c_out 9 \
  --des 'Exp' \
  --d_model 512 \
  --d_ff 512 \
  --itr 1 \
  --target_root_path D:/FPT/SU24/DSP391m/try/iTransformer/data/real/ \
  --target_data_path df_combine.csv \
  --lradj 'type1' \
  --learning_rate 0.0001 \
  --patience 5 \
  --moving_avg 10 \
  --dropout 0.25 \
  --train_epochs 20 \
  --batch_size 32 \
  --do_predict