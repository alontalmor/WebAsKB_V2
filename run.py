from config import *
from SplitQA import SplitQA
from noisy_supervision import NoisySupervision
#from webaskb_ptrnet import WebAsKB_PtrNet
from webaskb_ptr_vocab_net import WebAsKB_PtrVocabNet

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("operation", help='available operations: "gen_noisy_sup","run_ptrnet" ,"train_ptrnet", "splitqa"')
parser.add_argument("--eval_set", help='available eval sets: "dev","test"')
parser.add_argument("--name", help='name of output folder, as well as the whole experiment')
parser.add_argument("--data", help='define which directory to load input from (model dir for instance)')
parser.add_argument("--model", help='define which directory to load input from (model dir for instance)')

args = parser.parse_args()

# run dir will be created depending on the operation
#config.create_run_dir(args.run_tag,args.operation)

if args.eval_set is not None:
    config.EVALUATION_SET = args.eval_set
if args.name is not None:
    config.name = args.name
    config.out_subdir = config.name + '/'
if args.data is not None:
    config.input_data = args.data + '/'
if args.model is not None:
    config.input_model = args.model + '/'

if args.operation == 'gen_noisy_sup':
    noisy_sup = NoisySupervision()
    noisy_sup.gen_noisy_supervision()
elif args.operation == 'run_model':
    ptrnet = WebAsKB_PtrVocabNet()
    ptrnet.load_data(config.noisy_supervision_dir ,'train', config.EVALUATION_SET)
    ptrnet.init()
    ptrnet.eval()

elif args.operation == 'train_supervised':
    config.PERFORM_TRAINING = True
    config.LOAD_SAVED_MODEL = False
    config.max_evalset_size = 2000
    ptrnet = WebAsKB_PtrVocabNet()
    ptrnet.load_data(config.noisy_supervision_dir ,'train', config.EVALUATION_SET)
    ptrnet.init()
    ptrnet.train()

elif args.operation == 'preproc_RL':
    ptrnet = WebAsKB_PtrVocabNet()
    ptrnet.preproc_rl_data()

elif args.operation == 'train_RL':
    config.PERFORM_TRAINING = True
    config.LOAD_SAVED_MODEL = True
    config.RL_Training = True
    config.always_save_model = True
    config.max_evalset_size = 2000
    config.evaluate_every = 3000
    config.MAX_ITER = 9001

    config.LR = 0.00017
    config.ADA_GRAD_LR_DECAY = 0
    config.ADA_GRAD_L2 = 3e-4


    # In RL we always use teacher forcing (input to next step is always
    # as in the RL trajectory)
    config.teacher_forcing_full_until = float("inf")

    ptrnet = WebAsKB_PtrVocabNet()
    ptrnet.load_data(config.rl_preproc_data + config.input_data ,'train', config.EVALUATION_SET)
    ptrnet.init()
    ptrnet.train()

elif args.operation == 'splitqa':
    config.PERFORM_TRAINING = False
    splitqa = SplitQA()
    splitqa.run_executors()
    splitqa.compute_final_results()