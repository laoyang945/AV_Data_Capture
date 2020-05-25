import argparse
from core import *
from number_parser import get_number


def check_update(local_version):
    data = json.loads(get_html("https://api.github.com/repos/yoshiko2/AV_Data_Capture/releases/latest"))

    try:
        remote = float(data["tag_name"])
        local = float(local_version)
    except ValueError:
        print("[-] Check update failed! Skipped.")
        return

    download_url = data["html_url"]

    if local < remote:
        line1 = "* New update " + str(remote) + " *"
        print("[*]" + line1.center(54))
        print("[*]" + "↓ Download ↓".center(54))
        print("[*] " + download_url)
        print("[*]======================================================")


def argparse_function() -> [str, bool]:
    parser = argparse.ArgumentParser()
    #parser.add_argument("path", default='.', nargs='?', help="Movie file path.")
    parser.add_argument("-c", "--config", default='config.ini', nargs='?', help="The config file Path.")
    parser.add_argument("-a", "--auto-exit", dest='autoexit', action="store_true", help="Auto exit after program complete")
    args = parser.parse_args()

    return args.config, args.autoexit

def movie_lists(root, escape_folder):
    for folder in escape_folder:
        if folder in root:
            return []
    total = []
    file_type_re = re.compile('\.(mp4|avi|mpg|divx|rmvb|wmv|mov|mkv|flv|ts|webm)$', re.I)
    dirs = os.listdir(root)
    for entry in dirs:
        f = os.path.join(root, entry)
        if os.path.isdir(f):
            total += movie_lists(f, escape_folder)
        elif file_type_re.search(os.path.splitext(f)[1]):
            if not re.search(r'UU|APP|papapa', f, re.I):
                total.append(f)
    return total


def create_failed_folder(failed_folder):
    if not os.path.exists(failed_folder + '/'):  # 新建failed文件夹
        try:
            os.makedirs(failed_folder + '/')
        except:
            print("[-]failed!can not be make folder 'failed'\n[-](Please run as Administrator)")
            os._exit(0)


def CEF(path):
    try:
        files = os.listdir(path)  # 获取路径下的子文件(夹)列表
        for file in files:
            os.removedirs(path + '/' + file)  # 删除这个空文件夹
            print('[+]Deleting empty folder', path + '/' + file)
    except:
        a = ''


def create_data_and_move(file_path: str, c: config.Config):
    # Normalized number, eg: 111xxx-222.mp4 -> xxx-222.mp4
    n_number = get_number(file_path)

    try:
        print("[!]Making Data for [{}], the number is [{}]".format(file_path, n_number))
        core_main(file_path, n_number, c)
        print("[*]======================================================")
    except Exception as err:
        print("[-] [{}] ERROR:".format(file_path))
        print('[-]', err)

        if c.soft_link():
            print("[-]Link {} to failed folder".format(file_path))
            os.symlink(file_path, str(os.getcwd()) + "/" + conf.failed_folder() + "/")
        else:
            try:
                abc = ''
                # print("[-]Move [{}] to failed folder".format(file_path))
                # shutil.move(file_path, conf.failed_folder())
            except Exception as err:
                print('[!]', err)


if __name__ == '__main__':
    version = '3.4'

    # Parse command line args
    config_file, auto_exit = argparse_function()

    # Read config.ini
    conf = config.Config(path=config_file)

    version_print = 'Version ' + version
    print('[*]================== AV Data Capture ===================')
    print('[*]' + version_print.center(54))
    print('[*]======================================================')

    #if conf.update_check():
    #    check_update(version)

    create_failed_folder(conf.failed_folder())
    download_path = '.' if conf.movie_path() == '' else conf.movie_path()
    movie_list = movie_lists(download_path, re.split("[,，]", conf.escape_folder()))

    #    CEF(conf.success_folder())
    #    CEF(conf.failed_folder())
    count = 0
    count_all = str(len(movie_list))
    print('processing ', download_path)
    print('[+]Find', count_all, 'movies')
    if conf.soft_link():
        print('[!] --- Soft link mode is ENABLE! ----')
    for movie_path in movie_list:  # 遍历电影列表 交给core处理
        print('[!] --- processing: ' + movie_path)
        count = count + 1
        percentage = str(count / int(count_all) * 100)[:4] + '%'
        print('[!] - ' + percentage + ' [' + str(count) + '/' + count_all + '] -')
        create_data_and_move(movie_path, conf)

    #CEF(conf.success_folder())
    #CEF(conf.failed_folder())
    print("[+]All finished!!!")
    if auto_exit:
        exit(0)
    input("[+][+]Press enter key exit, you can check the error message before you exit.")
