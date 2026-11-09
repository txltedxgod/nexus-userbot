import sys
import io
import time
import os
import platform
import asyncio
from telethon.tl.custom import Message

from nexus.loader import BaseModule, module, command
from nexus.utils import format_duration, format_bytes

@module(
    name="Terminal",
    description="Developer power tools: async eval/exec, shell terminal, and hardware diagnostics.",
    author="txltedxgod",
    version="1.1.0"
)
class TerminalModule(BaseModule):
    @command(
        name="eval",
        description="Evaluate an async Python expression with execution latency.",
        usage=".eval <python expression>"
    )
    async def cmd_eval(self, message: Message, args: list):
        if not args:
            await message.edit(self.ui.warning("Usage: `.eval <expression>`"))
            return

        code = " ".join(args)
        start = time.perf_counter()
        
        # Build local environment
        loc = {
            "client": self.client,
            "message": message,
            "db": self.db,
            "ui": self.ui,
            "asyncio": asyncio,
            "time": time
        }
        
        try:
            # Check if code has await
            if "await" in code:
                exec_code = f"async def __ex(): return {code}\n__result = await __ex()"
                exec(f"async def __run():\n    return {code}", loc)
                result = await loc["__run"]()
            else:
                result = eval(code, {}, loc)

            elapsed = (time.perf_counter() - start) * 1000
            res_str = str(result)
            if len(res_str) > 1000:
                res_str = res_str[:1000] + "\n...[truncated]"

            card = self.ui.card(
                title="EVAL RESULT",
                fields={
                    "Latency": f"{elapsed:.2f} ms",
                    "Return Type": type(result).__name__,
                    "Output": f"\n```{res_str}```"
                },
                icon="terminal"
            )
            await message.edit(card)
        except Exception as e:
            await message.edit(self.ui.error(f"Eval Error:\n`{e}`"))

    @command(
        name="exec",
        description="Execute arbitrary Python code block capturing stdout & stderr.",
        usage=".exec <python code>"
    )
    async def cmd_exec(self, message: Message, args: list):
        if not args:
            await message.edit(self.ui.warning("Usage: `.exec <code>`"))
            return

        code = " ".join(args)
        stdout_capture = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = stdout_capture

        loc = {
            "client": self.client,
            "message": message,
            "db": self.db,
            "ui": self.ui
        }

        try:
            exec(
                f"async def __exec_fn():\n" + "\n".join(f"    {line}" for line in code.split("\n")),
                {},
                loc
            )
            await loc["__exec_fn"]()
            sys.stdout = old_stdout
            out = stdout_capture.getvalue().strip() or "Code executed with 0 stdout output."
            await message.edit(f"💻 **EXEC OUTPUT:**\n```python\n{out}\n```")
        except Exception as e:
            sys.stdout = old_stdout
            await message.edit(self.ui.error(f"Execution Error:\n`{e}`"))

    @command(
        name="sh",
        description="Execute a shell terminal command asynchronously.",
        usage=".sh <command>"
    )
    async def cmd_sh(self, message: Message, args: list):
        if not args:
            await message.edit(self.ui.warning("Usage: `.sh <command>`"))
            return

        cmd = " ".join(args)
        await message.edit(f"`Executing: {cmd}...`")

        start = time.perf_counter()
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        try:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=30.0)
            elapsed = (time.perf_counter() - start) * 1000

            out_text = stdout.decode("utf-8", errors="replace").strip()
            err_text = stderr.decode("utf-8", errors="replace").strip()
            combined = (out_text + "\n" + err_text).strip() or "Command completed with no output."

            if len(combined) > 1500:
                combined = combined[:1500] + "\n...[truncated]"

            status_icon = "check" if proc.returncode == 0 else "cross"
            res = (
                f"{self.ui.ICONS[status_icon]} **TERMINAL (Exit: {proc.returncode})** `[{elapsed:.1f}ms]`\n"
                f"```bash\n$ {cmd}\n{combined}\n```"
            )
            await message.edit(res)
        except asyncio.TimeoutError:
            proc.kill()
            await message.edit(self.ui.error("Command execution timed out (30s limit)."))

    @command(
        name="sys",
        description="Display hardware and host operating system statistics.",
        usage=".sys"
    )
    async def cmd_sys(self, message: Message, args: list):
        uname = platform.uname()
        uptime_sec = time.time() - self.client.start_time
        
        fields = {
            "OS": f"{uname.system} {uname.release} ({uname.machine})",
            "Python": f"{platform.python_version()} ({platform.python_implementation()})",
            "Node / Host": uname.node,
            "CPU Cores": os.cpu_count() or 1,
            "Process Uptime": format_duration(uptime_sec),
            "Loaded Modules": len(self.client.modules.modules),
            "Registered Commands": len(self.client.modules.commands)
        }
        await message.edit(self.ui.card(title="SYSTEM DIAGNOSTICS", fields=fields, icon="stats"))
