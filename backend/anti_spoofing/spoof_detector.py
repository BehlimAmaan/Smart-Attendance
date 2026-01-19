import torch
import cv2
import os
from torchvision import transforms
from PIL import Image

from .model import MiniFASNetV2


class SpoofDetector:
    """
    CNN-based spoof detector using MiniFASNetV2 (80x80)
    """

    def __init__(self):
        self.device = torch.device("cpu")

        self.model = MiniFASNetV2(
            embedding_size=128,
            conv6_kernel=(5, 5),   
            drop_p=0.2,
            num_classes=3,       
            img_channel=3
        ).to(self.device)

        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(base_dir, "2.7_80x80_MiniFASNetV2.pth")

        state_dict = torch.load(model_path, map_location=self.device)

        
        clean_state = {
            k.replace("module.", ""): v for k, v in state_dict.items()
        }

        self.model.load_state_dict(clean_state, strict=True)
        self.model.eval()

        self.transform = transforms.Compose([
            transforms.Resize((80, 80)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.5, 0.5, 0.5],
                std=[0.5, 0.5, 0.5]
            )
        ])

    def is_real(self, face_img):
        if face_img is None:
            return False

        import cv2
        from PIL import Image
        import torch

        face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
        face_img = Image.fromarray(face_img)

        tensor = self.transform(face_img).unsqueeze(0).to(self.device)

        with torch.no_grad():
            logits = self.model(tensor)
            probs = torch.softmax(logits, dim=1)

            spoof_score = probs[0][1].item()  
            print("SPOOF SCORE:", spoof_score)

        return spoof_score < 0.2


