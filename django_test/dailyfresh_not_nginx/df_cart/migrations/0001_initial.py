# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_user', '0002_address'),
        ('df_goods', '0002_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('goods_count', models.IntegerField(default=1, verbose_name='商品数目')),
                ('goods', models.ForeignKey(to='df_goods.Goods', verbose_name='商品')),
                ('passport', models.ForeignKey(to='df_user.Passport', verbose_name='账户')),
            ],
            options={
                'db_table': 's_cart',
            },
        ),
    ]
