-- KEYS[1] = bucket key
-- ARGV[1] = rate (req/sec)
-- ARGV[2] = capacity (burst)
-- ARGV[3] = max_queue_time (seconds)

local rate = tonumber(ARGV[1])
local capacity = tonumber(ARGV[2])
local max_queue = tonumber(ARGV[3])

local interval = 1 / rate

-- Redis authoritative time
local t = redis.call("TIME")
local now = tonumber(t[1]) + tonumber(t[2]) / 1e6

local data = redis.call(
  "HMGET", KEYS[1],
  "tokens", "ts", "next_ts"
)

local tokens = tonumber(data[1])
local last_ts = tonumber(data[2])
local next_ts = tonumber(data[3])

-- init
if tokens == nil then
  tokens = capacity
  last_ts = now
end

-- refill tokens
local delta = math.max(0, now - last_ts)
tokens = math.min(capacity, tokens + delta * rate)

-- FAST PATH: token available
if tokens >= 1 then
  tokens = tokens - 1

  redis.call("HMSET", KEYS[1],
    "tokens", tokens,
    "ts", now
  )

  redis.call("EXPIRE", KEYS[1], math.ceil(capacity / rate * 2))

  return {
    1,              -- allowed
    0,              -- queued
    0,              -- wait_time
    math.floor(tokens)
  }
end

-- SLOW PATH: virtual queue
next_ts = next_ts or now

-- allow burst compression
next_ts = math.max(next_ts, now - (capacity - 1) * interval)

local scheduled = math.max(now, next_ts)
local wait_time = scheduled - now

if wait_time > max_queue then
  return {
    0,              -- allowed
    0,              -- queued
    wait_time,
    0
  }
end

-- reserve slot
redis.call("HMSET", KEYS[1],
  "tokens", tokens,
  "ts", now,
  "next_ts", scheduled + interval
)

redis.call("EXPIRE", KEYS[1], math.ceil(max_queue * 2))

return {
  1,              -- allowed
  1,              -- queued
  wait_time,
  0
}