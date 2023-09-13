import json

import ddddocr

from configs import settings
from helpers import download, strings
from helpers.verify.base import Base


class DdddOcrVerify(Base):
    def same_shape(self, **kwargs):
        raise Exception("ddddocr验证码识别器暂未实现识别相同形状的验证码功能")

    def slide(self, **kwargs):
        gap_image_path = kwargs.get("gap_image_path", "") # 滑块图
        bg_image_path = kwargs.get("bg_image_path", "") # 背景图
        is_refresh = kwargs.get("is_refresh", False)  # 是否强制刷新缓存
        gap_resize = kwargs.get("gap_resize", None)
        bg_resize = kwargs.get("bg_resize", None)
        # 判断图片链接和图片路径是否都为空
        if gap_image_path == "" or bg_image_path == "":
            raise Exception("图片路径不能同时为空")
        # 如果图片为外部url，则下载图片
        if gap_image_path.startswith("http"):
            download_rs = download.download_image(gap_image_path, save_directory=settings.BASE_SLIDE_DIR,
                                                  filename="gap",
                                                  sub_directory=strings.calculate_md5(gap_image_path),
                                                  resize=gap_resize)
            gap_image_path = download_rs.get("file_path")
        if bg_image_path.startswith("http"):
            download_rs = download.download_image(bg_image_path, save_directory=settings.BASE_SLIDE_DIR, filename="bg",
                                                  sub_directory=strings.calculate_md5(bg_image_path),
                                                  resize=bg_resize)
            bg_image_path = download_rs.get("file_path")

        # 判断缓存中是否已经存在解码结果
        md5_str = strings.calculate_md5(gap_image_path + ":" + bg_image_path)
        cache_key = f"ddddocr:slide:{md5_str}"
        # 调用云码SDK
        cache_data = self.get_cache_data(cache_key)
        if cache_data is None or is_refresh:
            # 调用带带弟弟SDK
            det = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)

            with open(gap_image_path, 'rb') as f:
                target_bytes = f.read()

            with open(bg_image_path, 'rb') as f:
                background_bytes = f.read()

            res = det.slide_match(target_bytes, background_bytes, simple_target=True)
            cache_data = {"x": float(res['target'][0]), "y": float(res['target'][1])}
            self.set_cache_data(cache_key, cache_data)
            return cache_data
        return cache_data
