
# Inter-Process Communication (IPC) Using Message Queues

This repository demonstrates **Inter-Process Communication (IPC)** using a shared memory queue on Windows. The project showcases how independent background processes pass data back and forth concurrently, and illustrates the difference between **asynchronous execution** and **process synchronization**.

---

## 🚀 How the System Works

The project is split into two distinct files to separate worker behaviors from system orchestration:

*   **`IPC_methods.py`**:  It contains only the definitions and logic for our worker processes (`P1` through `P4`). Running this file directly does nothing.
*   **`IPC.py`**:  This is the main orchestration script. It loads the `netpack` engine, sets up the shared queue environment, creates the processes, and executes them.

---

## 🛠️ Project Structure & Architecture

The script uses a control switch (`flag`) to toggle between two completely different experimental setups.

### SET-1 (`flag = 1`): Asynchronous Execution
Tests process behavior **without** synchronization.
*   **`P1` (Producer)**: Loops through integers `0` to `4` and pushes them into the shared queue.
*   **`P2` (Consumer)**: Sleeps for 1 second to let `P1` finish writing, then wakes up and empties the queue.
*   **Synchronization**: None. The main program triggers `P1` and `P2` and exits immediately without waiting.

### SET-2 (`flag = 2`): Process Synchronization
Tests process behavior **with** synchronization (`join_process`).
*   **`P3` (Producer/Consumer)**: Writes `0` to `4` into the queue, then immediately consumes the very first element (`0`) using a direct `.get()` call.
*   **`P4` (Consumer/Producer)**: Sleeps for 1 second, wakes up to read the remaining items (`1` to `4`), and then appends a new message (`1000`) to verify the queue is active.
*   **Synchronization**: Active. The main script freezes and waits for both background processes to fully terminate before finishing.

---

## 📊 Live Execution Logs & Analysis

Here are the exact outputs observed in the PowerShell terminal during testing:

### 1. SET-1 Output (`flag = 1`)
```text
Main ends
P1 has been started
Printing from P1 & write Data = 0
Printing from P1 & write Data = 1
Printing from P1 & write Data = 2
Printing from P1 & write Data = 3
Printing from P1 & write Data = 4
P2 has been started
Printing from P2 & read Data = 0
Printing from P2 & read Data = 1
Printing from P2 & read Data = 2
Printing from P2 & read Data = 3
Printing from P2 & read Data = 4
```
> 💡 **Analysis**: `Main ends` prints at the **very top**. Because no `join_process()` blocks are used, the main script spins up the workers and dies instantly while the background processes continue running on their own.

### 2. SET-2 Output (`flag = 2`)
```text
P3 has been started
Printing from P3 & write Data = 0
Printing from P3 & write Data = 1
Printing from P3 & write Data = 2
Printing from P3 & write Data = 3
Printing from P3 & write Data = 4
[=] Reading in P3 & data is 0
P4 has been started
Printing from P4 & read Data = 1
Printing from P4 & read Data = 2
Printing from P4 & read Data = 3
Printing from P4 & read Data = 4
[=] Writing in P4 & the data is 1000
Main ends
```
> 💡 **Analysis**:  `Main ends` moves to the **absolute bottom**. The `npk.join_process()` lines force the console to block until every piece of queue data is successfully sent, received, and closed. Additionally, `P4` only reads `1` through `4` because `P3` snatched the `0` out of the FIFO queue right before `P4` woke up.

---

## ⚠️  Windows Setup Note

Because Windows handles process spawning differently than Linux/macOS, all execution components inside `IPC.py` must be protected by the `if __name__ == '__main__':` block. 

Failing to properly indent the  execution code inside this block will result in a `RuntimeError` or an `IndentationError`. 
```python
if __name__ == '__main__':
    # all configuration variables and sets are indented inside here!
    Q = npk.create_queue()
    flag = 2
```
