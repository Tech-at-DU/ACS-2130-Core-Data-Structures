# Hash Tables for AI Caching

⭐️ **GOAL:** Put a hash table in front of a slow, metered model call so repeat prompts come back instantly, then cap it with a time limit and an eviction rule.

<!-- omit in toc -->
## ⏱ Agenda

- [[**5m**] Attendance &amp; Announcements](#5m-attendance--announcements)
- [[**10m**] ☀️ Warm Up](#10m-️-warm-up)
- [[**35m**] 📚 TT: Why a Cache Is a Hash Map](#35m--tt-why-a-cache-is-a-hash-map)
- [[**10m**] 🌴 Break](#10m--break)
- [[**25m**] 💻 Activity 1: Wrap a Slow Model in a Dict](#25m--activity-1-wrap-a-slow-model-in-a-dict)
- [[**30m**] 💻 Activity 2: Add TTL, LRU Eviction, and a Hit Rate](#30m--activity-2-add-ttl-lru-eviction-and-a-hit-rate)
- [[**5m**] Wrap Up](#5m-wrap-up)

<!-- > -->

<!-- omit in toc -->
## 🏆 Objectives

*By the end of this session, you'll be able to&hellip;*

1. Explain why a response cache is a hash map from prompt key to model answer
1. Design a cache key that normalizes prompts and hashes long ones with `hashlib`
1. Measure the time and call count a cache saves on repeated prompts
1. Implement a time-to-live (TTL) and a least-recently-used (LRU) size cap with `OrderedDict`
1. Decide when caching an artificial intelligence (AI) answer is the wrong move

<!-- > -->

## [**5m**] Attendance &amp; Announcements

<!-- > -->

## [**10m**] ☀️ Warm Up

Here is the stand-in for a large language model (LLM) call that we use all session. It sleeps about one second and counts every call, the same two things that hurt with a hosted model: latency and a metered bill. No application programming interface (API) keys needed.

```python
import time

calls = 0


def fake_llm(prompt):
    """Pretend model: slow (about 1 s) and metered (every call counts)."""
    global calls
    calls += 1
    time.sleep(1)
    return f"[model answer for: {prompt}]"
```

Paste it into a new file, `llm_cache.py`. Then, on paper or in a comment, answer one question: a help-desk bot gets "How do I reset my password?" 300 times a day. How many of those 300 calls does the model actually need to answer?

> **📈 PROTIP:** The same wrapper pattern works around a real software development kit (SDK) call. Swap the body of `fake_llm` for your provider's client call and nothing else in today's code changes.

<!-- > -->

## [**35m**] 📚 TT: Why a Cache Is a Hash Map

This is the talk track (TT) for today. You've already built a hash table from scratch. Today one of them earns its keep.

### The Bill Nobody Expected

Picture a log from a support bot on a quiet Tuesday:

```text
10:02:11  prompt="How do I reset my password?"   1.1s  billed
10:02:40  prompt="how do i reset my password?"   1.0s  billed
10:03:05  prompt="How do I reset my password? "  1.2s  billed
10:03:52  prompt="How do I reset my password?"   1.1s  billed
```

Four calls. One question. Every line paid for the same answer and made someone wait a second for it. The fix is older than any model: remember the answer.

### A Cache Is a Dict With a Policy

A cache is a hash map. The key is the prompt (or something built from it). The value is the response. A Python `dict` is already a hash table, so a lookup costs O(1) on average. Compare that to a model call that costs about a second and real money.

```python
cache = {}

def cached_llm(prompt):
    if prompt in cache:
        return cache[prompt]       # hit: no model call
    answer = fake_llm(prompt)      # miss: pay once
    cache[prompt] = answer
    return answer
```

Python ships a version of this already. `functools.lru_cache` memoizes a function by its arguments and reports hits and misses:

```python
from functools import lru_cache


@lru_cache(maxsize=128)
def cached_fake_llm(prompt):
    return fake_llm(prompt)


cached_fake_llm("What is a hash table?")
cached_fake_llm("What is a hash table?")
cached_fake_llm("what is a hash table?")
print(cached_fake_llm.cache_info())
# CacheInfo(hits=1, misses=2, maxsize=128, currsize=2)
```

> **💬 ASK AUDIENCE:** Look at that output. Why is the third call a miss when a human would call it the same question?

<details>
<summary>Answer</summary>

`lru_cache` keys on the exact argument. `"What"` and `"what"` are different strings, so they hash to different slots. The cache has no idea they mean the same thing. That is a key-design problem, and it is ours to solve.

</details>

### Normalize the Key

Two prompts that should share an answer need to produce the same key. The cheap fix: lowercase and collapse whitespace.

```python
def normalize(prompt):
    return " ".join(prompt.lower().split())
```

Now all four log lines above map to `"how do i reset my password?"`. One miss, three hits.

Normalization has a cost, though. Lowercasing is fine for "reset my password." It is wrong for "explain the `HashMap` class," where case carries meaning. Normalize only what you are sure doesn't change the answer.

### Hash Long Prompts

Real prompts carry pasted documents, chat history, and system instructions. Using a 40,000-character string as a dict key works, but it bloats memory and makes keys painful to log or store in an external cache. Hash it down instead. SHA-256 (Secure Hash Algorithm, 256-bit) from `hashlib` always gives a 64-character hex string:

```python
import hashlib

MODEL = "fake-model-v1"


def cache_key(prompt, model=MODEL):
    text = model + "\n" + normalize(prompt)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


print(len(cache_key("x" * 50_000)))  # 64
```

Notice the model name is part of the key. Upgrade the model and the old answers stop matching, which is what you want.

> **💬 QUICK CHECK:** What is missing from this key? `key = normalize(prompt)` for a bot that serves two models and lets callers set `temperature`.

<details>
<summary>Answer</summary>

Everything else that changes the answer: the model name and the sampling settings such as `temperature`. If two requests would get different answers, they need different keys.

</details>

### Collisions and Why Key Design Matters

Python's `dict` handles hash collisions for you. When two keys land in the same slot, it compares the keys with `==`, so a collision inside the table never hands back the wrong value.

The danger is collisions *you* create by throwing away information. Two ways teams get there:

1. Over-normalizing. Strip punctuation and `"Is 0.1 + 0.2 == 0.3?"` starts sharing a key with `"Is 01 02 03?"`.
1. Truncating the hash. Someone keeps the first few hex characters "to save space."

Here is what truncation does:

```python
import hashlib


def short_key(prompt, chars):
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:chars]


def first_collision(chars):
    seen = {}
    i = 0
    while True:
        prompt = f"question {i}"
        key = short_key(prompt, chars)
        if key in seen:
            return seen[key], prompt, key
        seen[key] = prompt
        i += 1


print(first_collision(2))  # ('question 9', 'question 15', '88')
print(first_collision(4))  # ('question 38', 'question 130', 'f607')
```

With two hex characters there are only 256 possible keys, and two prompts share one after 16 tries. Four characters gives 65,536 keys and still collides at 131 prompts. That is the birthday problem. When those keys collide, the dict's `==` check can't save you, because the two keys really are equal. Prompt B gets prompt A's answer. Keep the full digest.

> **💬 YOUR TURN:** Predict: with the full 64-character SHA-256 key, should you write code to handle two different prompts producing the same key?

<details>
<summary>Answer</summary>

No. Collisions are possible in theory, but with 2^256 possible values you won't hit one in practice. Spend that effort on key design: what goes into `normalize` and what context belongs in the key.

</details>

### Bound It: TTL and LRU

A dict that only grows is a memory leak with good intentions. Two limits fix it:

- A TTL (time to live) makes each entry expire after N seconds, so stale answers age out.
- A size cap with LRU (least recently used) eviction drops the entry nobody has asked for in the longest time once the cache is full.

`collections.OrderedDict` gives you LRU almost for free. `move_to_end(key)` marks a key as most recent. `popitem(last=False)` removes the oldest. For TTL, store an expiry time next to each value and read the clock with `time.monotonic()`, which can't go backwards when the system clock changes.

I'll be honest: we skip distributed caches (Redis and friends) today. The data structure is the same; the network is the hard part.

### When Caching AI Output Is Wrong

A cache returns the same answer every time. Sometimes that is the bug.

| Prompt | Cache it? | Why |
| --- | --- | --- |
| "How do I reset my password?" | Yes | Same answer for everyone |
| "Summarize my last five emails" | No | Personalized: the answer depends on who asks |
| "Give me three fresh team names" | No | The caller wants a new answer each time |
| "What's on the menu today?" | Short TTL only | Correct today, wrong tomorrow |

> **💬 ASK QUESTION:** A or B? A cache key of `normalize(prompt)` for "Summarize my last five emails," or skip the cache for that prompt.

<details>
<summary>Answer</summary>

B. With key A, the second user gets the first user's email summary, which is a privacy incident. If you must cache personalized output, the user ID has to be in the key, and even then a short TTL is usually right.

</details>

<!-- > -->

## [**10m**] 🌴 Break

<!-- > -->

## [**25m**] 💻 Activity 1: Wrap a Slow Model in a Dict

> **✅ DONE WHEN:** your script prints a no-cache time near 5 s with 5 model calls and a cached time near 2 s with 2 model calls.

1. Open `llm_cache.py` from the warm up. Under `fake_llm`, paste `normalize` and a dict-backed wrapper:

    ```python
    def normalize(prompt):
        return " ".join(prompt.lower().split())


    cache = {}


    def cached_llm(prompt):
        key = normalize(prompt)
        if key in cache:
            return cache[key]
        answer = fake_llm(prompt)
        cache[key] = answer
        return answer
    ```

1. Paste the timing harness at the bottom. `time.perf_counter()` is the right clock for measuring short durations:

    ```python
    prompts = [
        "What is a hash table?",
        "what is a  hash table?",
        "  What is a hash table?",
        "Explain LRU eviction.",
        "explain LRU eviction.",
    ]

    start = time.perf_counter()
    for p in prompts:
        fake_llm(p)
    print(f"no cache: {time.perf_counter() - start:.1f}s, model calls: {calls}")

    calls = 0
    start = time.perf_counter()
    for p in prompts:
        cached_llm(p)
    print(f"cached:   {time.perf_counter() - start:.1f}s, model calls: {calls}")
    ```

1. Run it with `python3 llm_cache.py`. You should see:

    ```text
    no cache: 5.0s, model calls: 5
    cached:   2.0s, model calls: 2
    ```

1. Swap the key for the hashed version from the talk track. Paste `import hashlib`, `MODEL`, and `cache_key` near the top, then change `key = normalize(prompt)` to `key = cache_key(prompt)`. Re-run. The numbers should not change.
1. Add one prompt to the list that *should* miss, and one that should hit. Re-run and confirm the call count moves the way you predicted.

> **‼️ WATCH OUT:** Running the file twice does not reuse the cache. The `cache` dict lives in memory and dies with the process. That is fine for today; a cache that survives restarts needs a store outside the process.

<!-- > -->

## [**30m**] 💻 Activity 2: Add TTL, LRU Eviction, and a Hit Rate

> **✅ READY WHEN:** the driver prints `hits=2 misses=4 rate=0.33 calls=4`, then after the TTL wait prints `after TTL: misses=5 calls=5 size=2`.

1. Paste this starter class into `llm_cache.py`, below `cache_key`. The constructor and `hit_rate` are done; `get` and `put` are yours.

    ```python
    from collections import OrderedDict


    class LLMCache:
        def __init__(self, max_size=2, ttl=3.0, clock=time.monotonic):
            self.max_size = max_size
            self.ttl = ttl
            self.clock = clock
            self.store = OrderedDict()  # key -> (expires_at, answer)
            self.hits = 0
            self.misses = 0

        def get(self, key):
            # TODO: miss if absent or expired (delete expired entries),
            # otherwise mark as most recently used and return the answer.
            raise NotImplementedError

        def put(self, key, answer):
            # TODO: store (expires_at, answer), mark as most recent,
            # then evict from the oldest end while over max_size.
            raise NotImplementedError

        def hit_rate(self):
            total = self.hits + self.misses
            return self.hits / total if total else 0.0
    ```

1. Write `get`. On a hit, call `self.store.move_to_end(key)` and add one to `self.hits`. On a missing or expired entry, add one to `self.misses` and return `None`. Expired means `self.clock() >= expires_at`.
1. Write `put`. Store `(self.clock() + self.ttl, answer)`, call `move_to_end`, then `popitem(last=False)` in a loop while `len(self.store) > self.max_size`.
1. Comment out the Activity 1 timing harness, then paste this driver at the bottom and run it:

    ```python
    lru = LLMCache(max_size=2, ttl=3.0)
    calls = 0


    def ask(prompt):
        key = cache_key(prompt)
        answer = lru.get(key)
        if answer is None:
            answer = fake_llm(prompt)
            lru.put(key, answer)
        return answer


    for p in [
        "What is a hash table?",
        "what is a hash table?",
        "Explain LRU eviction.",
        "What is a hash table?",
        "Define TTL.",
        "Explain LRU eviction.",
    ]:
        ask(p)
    print(f"hits={lru.hits} misses={lru.misses} rate={lru.hit_rate():.2f} calls={calls}")

    time.sleep(3.1)
    ask("Define TTL.")
    print(f"after TTL: misses={lru.misses} calls={calls} size={len(lru.store)}")
    ```

1. Before you run it, trace the six prompts on paper with a cap of 2. Write which key gets evicted on each miss. Then run and compare.
1. Post this in the team thread when you're done or stuck:

    ```text
    Built:
    Verified:
    Blocked by:
    Next:
    ```

> **📈 TIP:** Watch the hit rate as closely as the speed. A cache with a 5% hit rate is mostly overhead. Log `hit_rate()` and you'll know whether the key design is working.
> **FINISHED EARLY?** Pass a fake clock, such as `lambda: now[0]` with `now = [0.0]`, as `clock=` and test expiry without `time.sleep`.

<!-- > -->

## [**5m**] Wrap Up

- Finish `get` and `put` if the driver output doesn't match yet.
- Push `llm_cache.py` to your course repo and link it in your checkpoint.
- Stuck on eviction order? Print `list(lru.store)` after every `ask` call. The oldest key is first.

<!-- > -->

## Additional Resources

1. [Python docs: `functools.lru_cache`](https://docs.python.org/3/library/functools.html#functools.lru_cache)
1. [Python docs: `hashlib`](https://docs.python.org/3/library/hashlib.html)
1. [Python docs: `collections.OrderedDict`](https://docs.python.org/3/library/collections.html#collections.OrderedDict)
1. [Python docs: `time.monotonic`](https://docs.python.org/3/library/time.html#time.monotonic) and [`time.perf_counter`](https://docs.python.org/3/library/time.html#time.perf_counter)
1. [Python wiki: Time Complexity of built-in types](https://wiki.python.org/moin/TimeComplexity)
1. [Wikipedia: Cache replacement policies (LRU)](https://en.wikipedia.org/wiki/Cache_replacement_policies#LRU)
1. [Wikipedia: Birthday problem](https://en.wikipedia.org/wiki/Birthday_problem)

<details>
<summary>For Curriculum Authors</summary>

## For Curriculum Authors

### In Class

- MVP (15 minutes or less): get Activity 1 printing 5 calls uncached and 2 calls cached, then post the checkpoint paste.
- Open a fresh `llm_cache.py` and keep the log snippet from the opening section on screen during TT.
- Breakouts of 3–4 for both activities. Visit rooms; early finishers help a stuck room.
- After Activity 1, debrief one surprise: a prompt someone expected to hit that missed, or the reverse.
- The checkpoint paste (Built / Verified / Blocked by / Next) goes in the team thread. Anyone who missed the session can post it later from the reference solution below with no penalty.

### Facilitator Notes

- Live-code `cached_llm` and the `lru_cache` demo only. Then get out of the way.
- Expect the room to hit two bugs in Activity 2: forgetting `move_to_end` in `get` (eviction order goes FIFO, first in first out) and evicting before inserting. Have them print `list(lru.store)` to see it.
- `answer is None` as the miss signal breaks if a model ever returns `None`. Fine for today; mention it if someone asks.
- Reference solution for Activity 2, tested on Python 3.13:

    ```python
    def get(self, key):
        entry = self.store.get(key)
        if entry is None:
            self.misses += 1
            return None
        expires_at, answer = entry
        if self.clock() >= expires_at:
            del self.store[key]
            self.misses += 1
            return None
        self.store.move_to_end(key)
        self.hits += 1
        return answer

    def put(self, key, answer):
        self.store[key] = (self.clock() + self.ttl, answer)
        self.store.move_to_end(key)
        while len(self.store) > self.max_size:
            self.store.popitem(last=False)
    ```

- Trace for the driver with a cap of 2: miss, hit, miss, hit, miss (evicts "Explain LRU"), miss (evicts "What is a hash table?"). Final store holds "Define TTL." and "Explain LRU eviction."

### Expert Follow-Ups

- Compare `functools.lru_cache` with the hand-built class: what does `lru_cache` lack for AI responses? (TTL, custom keys, skipping errors.)
- Semantic caching keys on meaning (embeddings) instead of exact text. Good stretch discussion; it trades hash-table certainty for fuzzy matches.

</details>
