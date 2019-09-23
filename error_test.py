from re import findall


class ErrorTest:
    def __init__(self, title, desc, func):
        self.title = title
        self.desc = desc
        self.func = func

    def run_test(self, cpp_file):
        return self.func(cpp_file)

    @staticmethod
    def check_header_comment(class_no):
        def to_return(cpp_file):
            with open(cpp_file, encoding='utf-8') as code_file:
                codes = code_file.read()

                for comment in findall(r'/\*([\s\S]*?)\*/', codes) + findall(r'//.*', codes):
                    stripped = comment.replace('\n', '').replace('\t', '').replace(' ', '').lower()
                    if class_no in stripped:
                        return True
                return False

        return to_return

    @staticmethod
    def get_function_contains(content):
        def to_return(cpp_file):
            with open(cpp_file, encoding='utf-8') as code_file:
                codes = code_file.read()

                return bool(findall(content, codes))

        return to_return
