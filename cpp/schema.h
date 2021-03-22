#ifndef SCHEMA_H
#define SCHEMA_H

#include <string>
#include "nlohmann/json.hpp"

namespace thuai {
  using json = nlohmann::json;

  const size_t EGG_COUNT = 15, PLAYER_COUNT = 12, PLAYER_PER_TEAM = 4;

  struct Vec2D {
    double x, y;
  };

  enum Team {
    RED, YELLOW, BLUE
  };

  enum PlayerMovement {
    STOPPED, WALKING, RUNNING, SLIPPED
  };
  NLOHMANN_JSON_SERIALIZE_ENUM(PlayerMovement, {
    {STOPPED, "stopped"},
    {WALKING, "walking"},
    {RUNNING, "running"},
    {SLIPPED, "slipped"},
  })

  struct PlayerStatus {
    Vec2D position; // coordinate of player
    Vec2D facing;  // which direction is the player facing?
    PlayerMovement status; // movement status
    int holding; // id of the egg being held
  };

  struct EggStatus {
    Vec2D position; // coordinate of egg
    int holder; // id of the player holding the egg
    int score; // score of egg
  };

  void to_json(json& j, const Vec2D& vec);
  void from_json(const json& j, Vec2D& vec);

  void to_json(json& j, const PlayerStatus& p);
  void from_json(const json& j, PlayerStatus& p);

  void to_json(json& j, const EggStatus& p);
  void from_json(const json& j, EggStatus& p);
}
#endif