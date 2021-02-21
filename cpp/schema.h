#ifndef SCHEMA_H
#define SCHEMA_H

#include <string>
#include "nlohmann/json.hpp"

namespace thuai {
  using json = nlohmann::json;

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
    Vec2D position;
    Vec2D facing;
    PlayerMovement status;
  };

  struct EggStatus {
    Vec2D position;
    int holder;
  };

  void to_json(json& j, const Vec2D& vec);
  void from_json(const json& j, Vec2D& vec);

  void to_json(json& j, const PlayerStatus& p);
  void from_json(const json& j, PlayerStatus& p);

  void to_json(json& j, const EggStatus& p);
  void from_json(const json& j, EggStatus& p);
}
#endif