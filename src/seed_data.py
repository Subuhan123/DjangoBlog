import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoblog.settings')
django.setup()

from django.contrib.auth import get_user_model
from campus.models import Club, Activity, Signup

U = get_user_model()
admin_user = U.objects.get(username='zyq')

# ---------- 社团（已存在则跳过） ----------
clubs_data = [
    dict(name='编程爱好者协会',
         description='面向全校的编程技术交流社团，定期举办算法竞赛、项目实战和技术分享会。'),
    dict(name='光影摄影社',
         description='记录校园生活与城市风光，定期组织外拍活动和作品展。'),
    dict(name='紫金跑步俱乐部',
         description='每周三、周六组织操场夜跑，鼓励健康生活方式。'),
    dict(name='公益志愿者服务队',
         description='参与社区服务、敬老院探访、环保宣传等志愿活动。'),
]

clubs = {}
for d in clubs_data:
    obj, created = Club.objects.get_or_create(
        name=d['name'],
        defaults={'description': d['description'], 'leader': admin_user}
    )
    clubs[d['name']] = obj
    print(('新建' if created else '已存在'), '社团:', obj.name)

# ---------- 活动 ----------
now = datetime.now()

activities_data = [
    dict(title='2026 秋季算法训练营（第一讲）',
         club=clubs['编程爱好者协会'],
         description='讲解动态规划基础，从背包问题到区间 DP，配套练习讲解。',
         location='图书馆三楼机房 302',
         capacity=60,
         start_time=now + timedelta(days=3, hours=2),
         end_time=now + timedelta(days=3, hours=5),
         signup_deadline=now + timedelta(days=2)),
    dict(title='校园秋景人像外拍',
         club=clubs['光影摄影社'],
         description='以校园银杏大道为拍摄地点，讲解人像构图与自然光运用。',
         location='银杏大道集合',
         capacity=25,
         start_time=now + timedelta(days=5, hours=1),
         end_time=now + timedelta(days=5, hours=4),
         signup_deadline=now + timedelta(days=4)),
    dict(title='周三夜跑 5 公里',
         club=clubs['紫金跑步俱乐部'],
         description='配速分两档：慢跑 7分/公里，快跑 5分30/公里。',
         location='南区操场',
         capacity=80,
         start_time=now + timedelta(days=1, hours=12),
         end_time=now + timedelta(days=1, hours=13),
         signup_deadline=now + timedelta(hours=20)),
    dict(title='敬老院周末探访',
         club=clubs['公益志愿者服务队'],
         description='前往雨花台区敬老院陪伴老人聊天、表演节目。',
         location='校门口集合',
         capacity=20,
         start_time=now + timedelta(days=9, hours=3),
         end_time=now + timedelta(days=9, hours=7),
         signup_deadline=now + timedelta(days=7)),
    dict(title='秋季羽毛球友谊赛',
         club=clubs['紫金跑步俱乐部'],
         description='男女双打混合赛制，现场抽签分组，赛后发奖品。',
         location='体育馆二楼',
         capacity=32,
         start_time=now + timedelta(days=12),
         end_time=now + timedelta(days=12, hours=4),
         signup_deadline=now + timedelta(days=10)),
]

for d in activities_data:
    obj, created = Activity.objects.get_or_create(
        title=d['title'],
        defaults={
            'club': d['club'],
            'description': d['description'],
            'location': d['location'],
            'capacity': d['capacity'],
            'start_time': d['start_time'],
            'end_time': d['end_time'],
            'signup_deadline': d['signup_deadline'],
            'status': 'open',
        }
    )
    print(('新建' if created else '已存在'), '活动:', obj.title)

print('\n===== 统计 =====')
print('社团总数:', Club.objects.count())
print('活动总数:', Activity.objects.count())
