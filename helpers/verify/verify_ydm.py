import json

from configs import settings
from helpers import download, strings
from helpers.verify.base import Base
from helpers.verify.sdk.ydm_verify import YdmVerify


class VerifyYdm(Base):
    """
    云码验证器
    """

    def __init__(self, **kwargs):
        self.token = kwargs.get("token")
        self.sdk = YdmVerify(token=self.token)

    def same_shape(self, **kwargs):
        """
        比对图片形状
        """
        image_path = kwargs.get("image_path", "") # 图片路径
        is_refresh = kwargs.get("is_refresh", False) # 是否强制刷新缓存
        # 判断图片链接和图片路径是否都为空
        if image_path == "":
            raise Exception("图片路径不能同时为空")
        # 如果图片为外部url，则下载图片
        if image_path.startswith("http"):
            download_rs = download.download_image(image_path, save_directory=settings.DIRS["BASE_CLICK_SAME_SHAPE_DIR"],
                                                  resize=kwargs.get("resize"),)
            image_path = download_rs.get("file_path")

        # 判断缓存中是否已经存在解码结果
        md5_str = strings.calculate_md5(image_path)
        cache_key = f"ydm:same_shape:{md5_str}"
        # 调用云码SDK
        cache_data = self.get_cache_data(cache_key)
        if cache_data is None or is_refresh:
            # 读取图片内容
            with open(image_path, 'rb') as f:
                image_content = f.read()
            # 调用云码SDK
            cache_data = self.sdk.click_verify(image=image_content, verify_type=30101)
            self.set_cache_data(cache_key, json.dumps(cache_data))
            return cache_data

        return json.loads(cache_data)

    def slide(self, **kwargs):
        """
        滑块验证
        """
        gap_image_path = kwargs.get("gap_image_path", "") # 滑块图
        bg_image_path = kwargs.get("bg_image_path", "") # 背景图
        is_refresh = kwargs.get("is_refresh", False) # 是否强制刷新缓存
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
        cache_key = f"ydm:slide:{md5_str}"
        # 调用云码SDK
        cache_data = self.get_cache_data(cache_key)
        if cache_data is None or is_refresh:
            # 读取缺口图片内容
            with open(gap_image_path, 'rb') as f:
                gap_image_content = f.read()
            # 读取背景图片内容
            with open(bg_image_path, 'rb') as f:
                background_image_content = f.read()
            # 调用云码SDK
            api_rs = self.sdk.slide_verify(slide_image=gap_image_content, background_image=background_image_content)
            cache_data = {"x": float(api_rs), "y": float(0)}
            self.set_cache_data(cache_key, json.dumps(cache_data))
            return cache_data

        return json.loads(cache_data)
