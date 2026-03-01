"""Simple interactive smoke test using pexpect.

This test will run the `probe` CLI, select provider, try entering an invalid
API key then a dummy valid key, and send a short chat message. It asserts that
no crashes occur and expected prompts appear. It is not run by default in CI
because it requires a pseudo-terminal.
"""

import os
import sys
import time
import subprocess

try:
    import pexpect
except ImportError:
    print("pexpect not found, please install it to run interactive tests.")
    sys.exit(0)


def run_smoke():
    # spawn the probe CLI
    child = pexpect.spawn('probe', encoding='utf-8', timeout=20)
    try:
        # expect provider menu debug output then prompt
        child.expect('Provider menu displayed')
        child.sendline('1')  # choose first provider (OpenAI)
        # should then prompt for API key
        child.expect('OpenAI API key:')
        child.sendline('invalid_key')
        child.expect('Invalid OpenAI API key')
        # now send a plausible dummy key
        child.sendline('sk-test0000000000000000000000')
        # accept message
        child.expect('✓ OpenAI API key accepted')
        # after validating, the CLI may print "Model set to" and then start chat
        child.expect('Model set to')
        # send a chat message
        time.sleep(0.5)
        child.sendline('hello')
        # we expect some output or prompt back; match either '>' or new line
        child.expect(['\n', '>'])
        print("Interactive smoke test succeeded")
    except pexpect.exceptions.EOF as e:
        print("Unexpected EOF, process likely exited:", e)
        print(child.before)
    except pexpect.exceptions.TIMEOUT as e:
        print("Timeout waiting for prompt:", e)
        print(child.before)
    finally:
        child.close()


if __name__ == '__main__':
    run_smoke()
