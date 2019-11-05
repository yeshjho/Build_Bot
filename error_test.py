from re import findall
from texts import TEXT


class ErrorTest:
    def __init__(self, title, desc, func):
        self.title = title
        self.desc = desc
        self.func = func

    def run_test(self, cpp_file):
        return self.func(cpp_file)
        
    @staticmethod
    def get_comments(code_text):
        return findall(TEXT.RE.COMMENT, code_text)

    @staticmethod
    def check_header_comment(class_no):
        def to_return(cpp_file):
            with open(cpp_file, encoding='utf-8') as code_file:
                codes = code_file.read()

                for comment in ErrorTest.get_comments(codes):
                    stripped = comment.replace('\n', '').replace('\t', '').replace(' ', '').lower()
                    if class_no in stripped:
                        return True
                return False

        return to_return

    @staticmethod
    def get_function_contains(*content, should_contain=True):
        def to_return(cpp_file):
            with open(cpp_file, encoding='utf-8') as code_file:
                codes = code_file.read()

                for comment in ErrorTest.get_comments(codes):
                    codes = codes.replace(comment, '')
                
                does_contain = False
                for to_match in content:
                    if findall(to_match, codes):
                        does_contain = True
                        break
                return does_contain if should_contain else not does_contain

        return to_return
