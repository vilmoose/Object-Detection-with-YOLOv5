import torch

def verify_args(args):
    if args.use_cuda and torch.cuda.is_available() == False:
        print("No GPU environment, set --use-cuda:False")
        exit(0)

    if args.thickness < 1 / args.resize_window:
        print("Please check (and adjust) the following parameter requirment: --thickness ")
        exit(0)

    if not (0 < args.region[0] <= 1) and not (0 < args.region[1] <= 1):
        print("Value must be between 0 and 1 for the follwing parameter: --region ")
        exit(0)

    if args.lock_button not in ['left', 'middle', 'right', 'x1', 'x2']:
        print("--lock-button only supports the following mouse buttons:left, middle, right, x1, x2")
        exit(0)

    for i in args.lock_choice:
        if i not in args.lock_tag:
            print("Please check (and adjust) the following parameter requirment: --lock-choice")
            exit(0)

    buttons = []
    buttons.append(args.lock_button)
    # if args.recoil_button_ak47 not in ['left', 'middle', 'right', 'x1', 'x2']:
    #    print("--recoil-button-ak47 only supports the following mouse buttons:left, middle, right, x1, x2")
    #    exit(0)
    # if args.recoil_button_ak47 in buttons:
    #   print("The following parameter conflicts with other keys: --recoil-button-ak47 ")
    #  exit(0)
    #buttons.append(args.recoil_button_ak47)

    # if args.recoil_button_m4a1 not in ['left', 'middle', 'right', 'x1', 'x2']:
    #     print("--recoil-button-m4a1 only supports the following mouse buttons:left, middle, right, x1, x2")
    #     exit(0)
    # if args.recoil_button_m4a1 in buttons:
    #     print("The following parameter conflicts with other keys: --recoil-button-m4a1")
    #     exit(0)
    # buttons.append(args.recoil_button_m4a1)
