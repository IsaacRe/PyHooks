from torchvision.models import resnet18
from torchvision.transforms import Compose, Resize, ToTensor
from torchvision.datasets import CIFAR100
from torch.utils.data import DataLoader
from tacklebox.hooks.model_tracking import ModuleTracker
import torch


if __name__ == '__main__':
    model = resnet18()
    model.cuda()

    dataset = CIFAR100('../data/', train=True, transform=Compose([Resize((224, 224)), ToTensor()]))
    loader = DataLoader(dataset)

    x, y = next(iter(loader))
    x = x.to(0)

    tracker = ModuleTracker(model.layer1[0].conv1, pooling=model.avgpool)
    with tracker.track():
        model(x).sum().backward()
        raw = tracker.gather()

    # try using category in HookManager context
    hookmngr = tracker.hook_manager
    with hookmngr.hook_all_context(category='forward_hook'):
        model(x).sum().backward()
        raw2 = tracker.gather()

    with hookmngr.hook_all_context(category='backward_hook'):
        model(x).sum().backward()
        raw3 = tracker.gather()

    pass
