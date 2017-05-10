#include "redismodule.h"
int TestCommand(RedisModuleCtx *ctx, RedisModuleString **argv, int argc) {

  return RedisModule_ReplyWithSimpleString(ctx, "OK");
}

int ErrCommand(RedisModuleCtx *ctx, RedisModuleString **argv, int argc) {
  return RedisModule_ReplyWithError(ctx, "ERR");
}

/* Registering the module */
int RedisModule_OnLoad(RedisModuleCtx *ctx, RedisModuleString **argv, int argc) {
  if (RedisModule_Init(ctx, "test", 1, REDISMODULE_APIVER_1) == REDISMODULE_ERR) {
    return REDISMODULE_ERR;
  }
  if (RedisModule_CreateCommand(ctx, "test.test", TestCommand, "readonly", 0,0,0) == REDISMODULE_ERR) {
    return REDISMODULE_ERR;
  }
  if (RedisModule_CreateCommand(ctx, "test.error", ErrCommand, "readonly", 0,0,0) == REDISMODULE_ERR) {
    return REDISMODULE_ERR;
  }
  return REDISMODULE_OK;
}