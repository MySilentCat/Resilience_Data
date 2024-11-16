import codecs
import os
import sys
import chardet


def ReadFile(filePath):
    file = open(filePath, 'rb')
    # 根据二进制信息判断编码{'encoding': 'ascii', 'confidence': 1.0, 'language': ''}
    encoding_message = chardet.detect(file.read())
    print(filePath, encoding_message['encoding'])
    file.close()
    if encoding_message["encoding"] is None:
        return None
    if encoding_message['encoding'] == "GB2312":
        encoding_message['encoding'] = "GBK"
    with codecs.open(filePath, "rb", encoding=encoding_message['encoding']) as f:
        return f.read()


def SaveAsUTF8(filePath):
    for root, dirs, files in os.walk(filePath):
        for file in files:
            if file.split(".")[-1] == "c" or file.split(".")[-1] == "h":
                path = os.path.join(root, file).replace("\\", "/").replace("//", "/")
                content = ReadFile(path)
                if content is not None:
                    with codecs.open(path, "w", encoding="utf-8") as f:
                        f.write(content)


if __name__ == '__main__':
    args = sys.argv
    SaveAsUTF8(
        r"D:\design_reconstruction\week47\chatroom-master\chatroom-master\code\src")
