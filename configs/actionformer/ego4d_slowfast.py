_base_ = [
    "../_base_/models/actionformer.py",  # model config
    "../_base_/datasets/ego4d_mq/features_slowfast_trunc.py",  # dataset config
]

model = dict(
    projection=dict(
        in_channels=2304,
        arch=(2, 2, 7),
        use_abs_pe=True,
        max_seq_len=1024,
        conv_cfg=dict(proj_pdrop=0.1),
        attn_cfg=dict(n_mha_win_size=9),
    ),
    neck=dict(type="FPNIdentity", num_levels=8),
    rpn_head=dict(
        num_classes=110,
        prior_generator=dict(
            strides=[1, 2, 4, 8, 16, 32, 64, 128],
            regression_range=[(0, 4), (2, 8), (4, 16), (8, 32), (16, 64), (32, 128), (64, 256), (128, 10000)],
        ),
    ),
)

solver = dict(
    train=dict(batch_size=2, num_workers=2),
    val=dict(batch_size=1, num_workers=1),
    test=dict(batch_size=1, num_workers=1),
    clip_grad_norm=1,
    ema=True,
)

optimizer = dict(type="AdamW", lr=1e-4, weight_decay=0.05, paramwise=True)
scheduler = dict(type="LinearWarmupCosineAnnealingLR", warmup_epoch=5, max_epoch=15)

inference = dict(load_from_raw_predictions=False, save_raw_prediction=False)
post_processing = dict(
    pre_nms_topk=5000,
    nms=dict(
        use_soft_nms=True,
        sigma=0.9,
        max_seg_num=2000,
        min_score=0.001,
        multiclass=True,
        voting_thresh=0.95,  #  set 0 to disable
    ),
    save_dict=False,
)

workflow = dict(
    logging_interval=200,
    checkpoint_interval=1,
    val_loss_interval=1,
    val_eval_interval=1,
    val_start_epoch=8,
)

work_dir = "exps/ego4d/actionformer_slowfast"
