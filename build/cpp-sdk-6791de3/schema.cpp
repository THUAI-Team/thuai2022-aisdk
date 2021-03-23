#include "schema.h"

namespace thuai {
  void to_json(json& j, const Vec2D& vec) {
    j = json{
      {"x", vec.x},
      {"y", vec.y}
    };
  }
  void from_json(const json& j, Vec2D& vec) {
    j.at("x").get_to(vec.x);
    j.at("y").get_to(vec.y);
  }

  void to_json(json& j, const PlayerStatus& p) {
    j = json{
      {"position", p.position},
      {"facing", p.facing},
      {"status", p.status}
    };
  }
  
  void from_json(const json& j, PlayerStatus& p) {
    j.at("position").get_to(p.position);
    j.at("facing").get_to(p.facing);
    j.at("status").get_to(p.status);
  }

  void to_json(json& j, const EggStatus& p) {
    j = json{
      {"position", p.position},
      {"holder", p.holder}
    };
  }

  void from_json(const json& j, EggStatus& p) {
    j.at("position").get_to(p.position);
    j.at("holder").get_to(p.holder);
  }
}