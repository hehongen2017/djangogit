本项目实现在线学习网站的搭建，实现注册，登录，找回密码，页面展示等功能。 

项目说明

开发环境
python (3.4.4)
Django (1.9)
MySQL (5.7)
windows(8.1)
数据库设计(models)

用户 user app model
机构 organization app model
课程 course app model
操作 operation app model
功能设计(views)

用户操作功能
登录（session和cookie机制）
注册（form表单提交，图片验证码，发送邮件）
找回密码（邮件发送）
信息修改（修改密码，头像，邮箱，基本信息）
全局搜索
消息提醒
课程机构功能
机构列表（分页，筛选，排序）
机构详情（收藏，富文本展示）
咨询提交（modelform验证与保存）
课程功能
课程列表（分页，排序）
课程详情（收藏，章节展示，资源展示，评论）
讲师功能
讲师列表（分页，排序）
讲师详情（收藏）
全局功能
全局404和500页面的配置
