BOT_NAME = 'voxybg'
SPIDER_MODULES = ['voxybg.spiders']
NEWSPIDER_MODULE = 'voxybg.spiders'
ROBOTSTXT_OBEY = True
LOG_LEVEL = 'WARNING'
ITEM_PIPELINES = {
    'voxybg.pipelines.VoxybgPipeline': 300,
}

