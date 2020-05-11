# Name: data_config
# Author: Reacubeth
# Time: 2020/3/31 13:56
# Mail: noverfitting@gmail.com
# Site: www.omegaxyz.com
# *_*coding:utf-8 *_*


def get_torchbiggraph_config():

    config = dict(
        # I/O data
        entity_path="rel9811",
        edge_paths=[
            "rel9811/train_p",
            "rel9811/valid_p",
            "rel9811/test_p",
        ],
        checkpoint_path="model/rel9811",

        # Graph structure
        entities={
            'all': {'num_partitions': 1},
        },
        relations=[{
            'name': 'all_edges',
            'lhs': 'all',
            'rhs': 'all',
            'operator': 'translation',
        }],
        dynamic_relations=True,

        # Scoring model
        dimension=50,
        global_emb=False,
        comparator='dot',

        # Training
        num_epochs=20,
        num_uniform_negs=500,
        num_batch_negs=500,
        batch_size=10000,
        loss_fn='softmax',
        lr=0.1,

        # Evaluation during training
        eval_fraction=0,  # to reproduce results, we need to use all training data
        eval_num_uniform_negs=0,
        eval_num_batch_negs=10000,
    )

    return config
