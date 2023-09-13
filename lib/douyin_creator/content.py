import os

from playwright.async_api import TimeoutError as PlaywrightTimeoutError

from configs import settings
from helpers import download, strings, log
from lib.douyin_creator.base import CreatorBase
from lib.douyin_creator.models.content_data_detail import ContentDataDetailPage
from lib.douyin_creator.models.content_data_list import ContentDataListPage
from lib.douyin_creator.models.content_upload_image_text import ContentUploadImageTextPage
from lib.douyin_creator.models.content_upload_video import ContentUploadVideoPage
from lib.exception_handler import exception_handler
from lib.exceptions import ActionException


class CreatorContent(CreatorBase):
    """
    创作平台-作品发布操作方法
    """

    @exception_handler
    def upload_video(self, request):
        """
        上传视频

        Args:
            request (dict): 请求对象，包含以下参数：
                - user_id (str): 用户ID，必填
                - video (str): 视频地址，必填
                - desc (str): 作品描述，必填
                - cover (str, optional): 封面图片地址
                - sync_to_toutiao (bool, optional): 是否同步到今日头条，默认为False
                - allow_download (bool, optional): 是否允许他人下载视频，默认为False
                - who_can_watch (str, optional): 观看权限类型，可选值为 "all"（公开，公开的情况下才可以同步到今日头条）、"fans"（好友可见）、"private"（仅自己可见）
                - publish_time (dict, optional): 定时发布时间，格式为字典，包含以下键值对：
                    - type (str): 发布时间类型，可选值为 "now"（立即发布）或 "delay"（定时发布）
                    - time (str): 发布时间，格式为 "YYYY-MM-DD HH:MM", 可选时间支持设置到2小时后及14天内

        Returns:
            dict: 执行结果的响应对象，包含以下属性：
                - code (int): 响应代码
                - message (str): 响应消息
                - data (any): 响应数据

        Raises:
            ActionException: 如果发生API错误，则抛出相应的错误代码

        """
        # 检查视频地址是否提供
        if request.get('video') is None:
            raise ActionException(ActionException.CODE_DOUYIN_FILE_LIST_EMPTY)

        # 检查作品描述是否提供
        if request.get('desc') is None:
            raise ActionException(ActionException.CODE_DOUYIN_DESCRIPTION_EMPTY)

        # 下载视频文件到本地
        file_path = download.download_file(
            request.get('video'),
            save_directory=settings.BASE_VIDEO_DIR,
            filename=strings.calculate_md5(request.get('video')),
        )
        if file_path is None:
            raise ActionException(ActionException.CODE_DOUYIN_VIDEO_FILE_DOWNLOAD_ERROR)
        request['video_path'] = file_path

        # 下载封面图片文件到本地
        if request.get('cover') is not None:
            cover_path = download.download_file(
                request.get('cover'),
                save_directory=settings.BASE_COVER_DIR,
                filename=strings.calculate_md5(request.get('cover')),
            )
            if cover_path is None:
                raise ActionException(ActionException.CODE_DOUYIN_VIDEO_COVER_DOWNLOAD_ERROR)
            request['cover_path'] = cover_path

        # 创建ContentUploadPage对象，表示发布内容的页面
        page = ContentUploadVideoPage(self.page)

        # 跳转到首页
        page.to_home()

        # 检查登录状态
        if self.check_login_state() is False:
            raise ActionException(ActionException.CODE_NOT_LOGIN)

        data = None
        # 等待页面加载完成
        self.page.wait_for_load_state(state="load")
        # 等待视频标签页出现
        page.tab_video().wait_for(timeout=10000, state="visible")

        # 点击发布视频标签页
        page.tab_video().click()

        # 等待上传按钮出现
        page.btn_upload().wait_for(timeout=10000, state="visible")

        # 设置上传文件路径为视频文件路径
        with self.page.expect_file_chooser() as fc_info:
            page.btn_upload().click()

        fc_info.value.set_files(request['video_path'])

        # 设置封面图片
        if request.get('cover_path') is not None:
            page.set_cover(request.get('cover_path'))

        # 填充作品描述
        page.text_description().fill(request.get('desc'))
        # 同步到今日头条
        if request.get('sync_to_toutiao') is not None:
            page.set_sync_toutiao(request.get('sync_to_toutiao'))

        # 允许他人下载视频
        if request.get('allow_download') is not None:
            page.set_download_content(request.get('allow_download'))

        # 设置谁可以看视频的选项
        if request.get('who_can_watch') is not None:
            page.set_who_can_watch(request.get('who_can_watch'))

        # 设置发布时间
        if request.get('publish_time') is not None:
            page.set_publish_time(request.get('publish_time'))

        # 等待视频上传完成，最长等待时间为5分钟
        page.btn_re_upload().wait_for(timeout=1000 * 5 * 60, state="visible")

        # 等待检测完成
        try:
            # 发文助手是否出现，否则等待检测结果出现
            page.semi_check_box().wait_for(timeout=1000, state="visible")
            page.semi_check_result_title().wait_for(state="visible")
            # 检查视频检测结果是否为正常
            if page.semi_check_result_title().inner_text() != "未见异常":
                raise ActionException(ActionException.CODE_DOUYIN_VIDEO_CHECK_ERROR,
                                   page.semi_check_result_content().inner_text())
        except ActionException as e:
            raise e
        except PlaywrightTimeoutError as e:
            log.logger.info("未检测到发文助手")

        # 捕获发布请求
        with self.page.expect_response(
                lambda response: "https://creator.douyin.com/web/api/media/aweme/create/" in response.url) as response_info:
            # 点击发布按钮
            page.btn_publish().click()
        # 等待页面加载完成，最长等待时间为5分钟
        self.page.wait_for_load_state(state="load", timeout=1000 * 60)

        if response_info.value is not None:
            json = response_info.value.json()
            data = {"aweme_id": json.get("aweme").get("aweme_id")}

        # 发布成功后清理下载的文件
        if request.get('video_path'):
            os.remove(request.get('video_path'))
        if request.get('cover_path'):
            os.remove(request.get('cover_path'))

        return data

    @exception_handler
    def upload_image_text(self, request):
        """
        发布图文

        Args:
            request (dict): 请求对象，包含以下参数：
                - user_id (str): 用户ID，必填
                - image_list (list): 图片地址列表，必填
                - cover (str, optional): 封面图片地址
                - title (str): 作品标题，必填
                - desc (str): 作品描述，必填
                - allow_download (bool, optional): 是否允许他人下载图片，默认为False
                - who_can_watch (str, optional): 观看权限类型，可选值为 "all"（公开）、"fans"（好友可见）、"private"（仅自己可见）
                - publish_time (dict, optional): 定时发布时间，格式为字典，包含以下键值对：
                    - type (str): 发布时间类型，可选值为 "now"（立即发布）或 "delay"（定时发布）
                    - time (str): 发布时间，格式为 "YYYY-MM-DD HH:MM"

        Returns:
            dict: 执行结果的响应对象，包含以下属性：
                - code (int): 响应代码
                - message (str): 响应消息
                - data (any): 响应数据

        Raises:
            ActionException: 如果发生API错误，则抛出相应的错误代码
        """
        # 检查图片地址列表是否提供
        if request.get('image_list') is None or len(request.get('image_list')) == 0:
            raise ActionException(ActionException.CODE_DOUYIN_IMAGE_LIST_EMPTY)
        # 下载图片文件到本地
        request['image_path_list'] = []
        for image in request.get('image_list'):
            file_path = download.download_file(
                image,
                save_directory=settings.BASE_IMAGE_DIR,
                filename=strings.calculate_md5(image),
            )
            if file_path is None:
                raise ActionException(ActionException.CODE_DOUYIN_VIDEO_FILE_DOWNLOAD_ERROR)
            request['image_path_list'].append(file_path)
        # 下载封面图片文件到本地
        if request.get('cover') is not None:
            cover_path = download.download_file(
                request.get('cover'),
                save_directory=settings.BASE_COVER_DIR,
                filename=strings.calculate_md5(request.get('cover')),
            )
            if cover_path is None:
                raise ActionException(ActionException.CODE_DOUYIN_VIDEO_COVER_DOWNLOAD_ERROR)
            request['cover_path'] = cover_path
        # 创建ContentUploadImageTextPage对象，表示发布内容的页面
        page = ContentUploadImageTextPage(self.page)
        # 跳转到首页
        page.to_home()
        # 检查登录状态
        if self.check_login_state() is False:
            raise ActionException(ActionException.CODE_NOT_LOGIN)
        data = None
        # 等待页面加载完成
        self.page.wait_for_load_state(state="load")
        # 等待图文标签页出现
        page.tab_image_text().wait_for(timeout=10000, state="visible")
        # 点击发布图文标签页
        page.tab_image_text().click()
        # 等待上传按钮出现
        page.set_upload_image(request['image_path_list'])
        # 等待图片上传完成，最长等待时间为5分钟
        page.btn_re_upload().wait_for(timeout=1000 * 5 * 60, state="visible")
        # 设置封面图片
        if request.get('cover_path') is not None:
            page.set_cover(request.get('cover_path'))
        # 填充作品标题
        page.text_title().fill(request.get('title'))
        # 填充作品描述
        page.text_description().fill(request.get('desc'))
        # 防止页面未加载完成
        self.page.wait_for_load_state(state="domcontentloaded")
        # 允许他人下载图片
        if request.get('allow_download') is not None:
            page.set_download_image(request.get('allow_download'))
        # 设置谁可以看
        if request.get('who_can_watch') is not None:
            page.set_who_can_watch(request.get('who_can_watch'))
        # 设置发布时间
        if request.get('publish_time') is not None:
            page.set_publish_time(request.get('publish_time'))
        # 捕获发布请求
        with self.page.expect_response(
                lambda response: "https://creator.douyin.com/web/api/media/aweme/create/" in response.url) as response_info:
            # 点击发布按钮
            page.btn_publish().click()
        # 等待页面加载完成，最长等待时间为1分钟
        self.page.wait_for_load_state(state="load", timeout=1000 * 60)

        if response_info.value is not None:
            json = response_info.value.json()
            data = {"aweme_id": json.get("aweme").get("aweme_id")}
        # 等待保存请求完成
        toast = page.toast()
        try:
            toast.wait_for(timeout=1000, state="visible")
            toast_text = toast.inner_text()
            if toast.is_visible() and toast_text != "":
                raise ActionException(ActionException.CODE_DOUYIN_VIDEO_COVER_UPLOAD_ERROR,
                                   "保存失败,错误内容为：" + toast_text)
        except ActionException as e:
            raise e
        except PlaywrightTimeoutError as e:
            log.logger.error("提示框不出现，继续执行", exc_info=True)
        except Exception as e:
            log.logger.error(e, exc_info=True)
            raise e
        # 发布成功后清理下载的文件
        if len(request.get('image_path_list')) > 0:
            for image_path in request.get('image_path_list'):
                os.remove(image_path)
        if request.get('cover_path'):
            os.remove(request.get('cover_path'))
        return data

    @exception_handler
    def get_data_list(self, request):
        """
        获取作品统计列表数据
        """
        # 创建ContentDataDetailPage对象，表示数据详情页面
        page = ContentDataListPage(self.page)

        # 检查登录状态
        if self.check_login_state() is False:
            raise ActionException(ActionException.CODE_NOT_LOGIN)
        data = []
        # 捕获发布请求
        with self.page.expect_response(
                lambda response: "https://creator.douyin.com/web/api/creator/data/item/summarize/" in response.url) as response_info:
            # 跳转到详情页
            page.to_home()
        # 等待页面加载完成，最长等待时间为5分钟
        self.page.wait_for_load_state(state="load", timeout=1000 * 60)

        if response_info.value is not None:
            json = response_info.value.json()
            if json.get("status_code") != 0:
                raise ActionException(ActionException.CODE_DOUYIN_DATA_LIST_ERROR, json.get("status_msg"))
            # 对json.get("item_list")进行处理，只保留statistics、summarize_data的字段
            for item in json.get("item_list"):
                data.append({
                    "user_id": self.user_id,
                    "aweme_id": item.get("aweme_id"),
                    "aweme_type": item.get("aweme_type"),
                    "statistics": item.get("statistics"),
                    "summarize_data": item.get("summarize_data"),
                })
        return data

    @exception_handler
    def get_data_detail(self, request):
        """
        获取作品详细数据
        """
        # 创建ContentDataDetailPage对象，表示数据详情页面
        page = ContentDataDetailPage(self.page)

        # 检查登录状态
        if self.check_login_state() is False:
            raise ActionException(ActionException.CODE_NOT_LOGIN)
        data = {}
        # 捕获发布请求
        with self.page.expect_response(
                lambda response: "https://creator.douyin.com/web/api/creator/data/item/summarize/" in response.url and f"&item_id={request.get('aweme_id')}" in response.url) as response_info:
            # 跳转到详情页
            page.to_home(request.get("aweme_id"))
        # 等待页面加载完成，最长等待时间为5分钟
        self.page.wait_for_load_state(state="load", timeout=1000 * 60)

        if response_info.value is not None:
            json = response_info.value.json()
            if json.get("status_code") != 0:
                raise ActionException(ActionException.CODE_DOUYIN_DATA_LIST_ERROR, json.get("status_msg"))
            # 对json.get("item_list")进行处理，只保留statistics、summarize_data的字段
            for item in json.get("item_list"):
                data = {
                    "user_id": self.user_id,
                    "aweme_id": item.get("aweme_id"),
                    "aweme_type": item.get("aweme_type"),
                    "statistics": item.get("statistics"),
                    "summarize_data": item.get("summarize_data"),
                }
        return data