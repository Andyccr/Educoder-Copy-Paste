"""
Author:Andyccr
Educoder-Copy-Paste-Crack


          .,-~~-.,          
       .~         ~.       
     ,'  ^^^  ^^^  ',     
    /   /\/\  /\/\   \    
   (   <<<>>>%%%     )    
    \   \/\/  \/\/   /    
     '.  ~~~  ~~~  ,'     
       ~._______.~        
          ~~~~~           


"""
import pyperclip
import pyautogui
import time
from pynput import keyboard
from threading import Event


class ClipboardTyper:
    def __init__(self):
        self.delay = 0.001  # 每个字符的输入延迟
        self.stop_event = Event()
        self.last_clipboard = ""
        self.combination_keys = set()  # 记录当前按下的键

    def type_clipboard_content(self):
        """模拟键盘输入剪贴板内容"""
        if self.stop_event.is_set():
            return

        try:
            text = pyperclip.paste()
            if not text or text == self.last_clipboard:
                return

            self.last_clipboard = text
            print(f"准备输入: {text[:50]}...")  # 只显示前50个字符

            # 给用户时间切换到目标窗口
            time.sleep(1)

            # 模拟键盘输入
            for char in text:
                if self.stop_event.is_set():
                    break
                pyautogui.typewrite(char)
                time.sleep(self.delay)

        except Exception as e:
            print(f"错误: {e}")

    def on_press(self, key):
        """按键按下时调用"""
        try:
            # 记录按下的键
            if key == keyboard.Key.cmd:
                self.combination_keys.add('cmd')
            elif hasattr(key, 'char') and key.char == 'b':
                self.combination_keys.add('b')

            # 检查是否是 cmd+b 组合键
            if {'cmd', 'b'}.issubset(self.combination_keys):
                self.type_clipboard_content()

        except AttributeError:
            pass

    def on_release(self, key):
        """按键释放时调用"""
        try:
            if key == keyboard.Key.cmd:
                self.combination_keys.discard('cmd')
            elif hasattr(key, 'char') and key.char == 'b':
                self.combination_keys.discard('b')

            # 按ESC键退出
            if key == keyboard.Key.esc:
                self.stop_event.set()
                return False  # 停止监听
        except AttributeError:
            pass
        return True

    def run(self):
        """主程序"""
        print("剪贴板输入工具已启动")
        print("使用方法:")
        print("1. 复制文本 (Command+C)")
        print("2. 在目标窗口按下 Command+B")
        print("3. 程序将模拟输入剪贴板内容")
        print("按下ESC键退出程序")

        # 启动键盘监听
        with keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:
            listener.join()


if __name__ == "__main__":
    # 安全设置
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.001

    try:
        typer = ClipboardTyper()
        typer.run()
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    finally:
        print("程序已退出")