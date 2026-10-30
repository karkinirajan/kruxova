# ********************
# imports vendors
# ********************
from celery import shared_task

# ********************
# imports shared
# ********************
from shared.data_caching import cache_to_files


@shared_task
def task_update_data_caches():
    """
    run action_save_data
    """
    cache_to_files.refresh()
