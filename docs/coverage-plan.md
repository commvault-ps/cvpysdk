# Increase Unit Test Coverage from 28% to 100%

## Context

The cvpysdk project has 52,271 statements across 287 source modules. Current unit tests (1,939 tests) cover 14,472 statements (28%). The uncovered 37,799 statements are mostly API-calling methods, property getters with lazy loading, and JSON construction — all of which can be tested with mocking (no live CommCell needed).

The codebase follows a highly uniform pattern: every entity holds `_commcell_object` → `_cvpysdk_object.make_request()` → `_services` dict. This means a single mocking strategy covers all 287 modules.

## Fixture Enhancements — `tests/conftest.py`

Before any test work, add these fixtures to the existing 3 (`mock_services`, `mock_commcell`, `mock_response`):

- **`make_entity`** — Factory to create any entity class with `__init__` bypassed (the `patch.object(cls, "__init__")` + `__new__` pattern already used in `test_commcell.py`, promoted to a reusable fixture)
- **`make_api_response`** — Returns `(flag, response)` tuples for `make_request` mocking, wrapping `mock_response`
- **`mock_client`** — Pre-configured mock Client with `client_id`, `client_name`, referencing `mock_commcell`
- **`mock_agent`** — Pre-configured mock Agent referencing `mock_client`
- **`mock_instance`** / **`mock_backupset`** — For subclient-level tests

Also add subdirectory conftest files:
- `tests/unit/subclients/virtualserver/conftest.py` — shared `mock_vs_subclient` fixture
- `tests/unit/instances/virtualserver/conftest.py` — shared `mock_vs_instance` fixture

## Phases

### Phase 1: Core Hierarchy (7 modules, ~3,700 new tests)

The largest coverage gaps. Each follows the Collection/Entity pattern.

| # | File | Missed | Current | New tests |
|---|------|--------|---------|-----------|
| 1 | `cvpysdk/commcell.py` | 1,467 | 22% | ~750 |
| 2 | `cvpysdk/client.py` | 2,560 | 11% | ~800 |
| 3 | `cvpysdk/job.py` | 670 | 24% | ~450 |
| 4 | `cvpysdk/plan.py` | 1,688 | 12% | ~500 |
| 5 | `cvpysdk/organization.py` | 835 | 25% | ~550 |
| 6 | `cvpysdk/instance.py` | 821 | 14% | ~270 |
| 7 | `cvpysdk/subclient.py` | 703 | 22% | ~380 |

**What to test per module:**
- All lazy-loading properties (getter returns `self._attr`, first access triggers `_get_*_properties()`)
- All property setters (call `update_properties()` or similar)
- All API-calling methods: success path, flag=False raises, empty response raises, bad input type raises
- Collection methods: `has_*()`, `get()`, `__getitem__`, `__len__`, `add_*()`, `delete()`
- `client.py` has ~30 `add_*` methods with identical patterns — use `@pytest.mark.parametrize` to cover all in one parametrized test

### Phase 2: Second-Level Entities (12 modules, ~2,600 new tests)

| File | Missed | New tests |
|------|--------|-----------|
| `cvpysdk/agent.py` | ~400 | ~100 |
| `cvpysdk/backupset.py` | 612 | ~200 |
| `cvpysdk/storage.py` | 765 | ~400 |
| `cvpysdk/policies/storage_policies.py` | 1,368 | ~500 |
| `cvpysdk/clientgroup.py` | 574 | ~260 |
| `cvpysdk/schedules.py` | 556 | ~230 |
| `cvpysdk/credential_manager.py` | 277 | ~150 |
| `cvpysdk/storage_pool.py` | 475 | ~190 |
| `cvpysdk/security/user.py` | 673 | ~250 |
| `cvpysdk/security/usergroup.py` | 466 | ~200 |
| `cvpysdk/security/role.py` | ~200 | ~80 |
| `cvpysdk/security/security_association.py` | ~200 | ~60 |

### Phase 3: Agent-Specific Subclasses (~80 modules, ~2,500 new tests)

These all inherit from base classes and override specific methods. Strategy:

- **`subclients/vssubclient.py`** (956 missed) — test thoroughly as the base for all 30 VS subclients (~300 tests)
- **`subclients/fssubclient.py`** (508 missed) — properties, backup/restore methods (~200 tests)
- **30 virtualserver subclients** — each has `full_vm_restore_in_place/out_of_place` + platform-specific methods. Use parametrized conftest. ~20 tests each (~600 total)
- **Other subclients** (db, sql, oracle, exchange, cloudapps, lotusnotes, etc.) — ~20 files, ~40-80 tests each (~900 total)
- **~30 instance subclasses** — override properties, ~15-40 tests each (~600 total)
- **~15 backupset subclasses** — minimal overrides, ~10-20 tests each (~200 total)

### Phase 4: Remaining Top-Level Modules (~30 modules, ~1,800 new tests)

Independent modules following the same Collection/Entity pattern:

`workflow.py` (~100), `alert.py` (~60), `network.py` (~80), `network_topology.py` (~60), `network_throttle.py` (~50), `index_server.py` (~100), `disasterrecovery.py` (~60), `eventviewer.py` (~40), `globalfilter.py` (~30), `domains.py` (~40), `operation_window.py` (~50), `download_center.py` (~40), `identity_management.py` (~40), `commcell_migration.py` (~40), `activitycontrol.py` (~30), `array_management.py` (~30), `additional_settings.py` (~30), `hac_clusters.py` (~30), `certificates.py` (~20), `name_change.py` (~20), `content_analyzer.py` (~40), `deduplication_engines.py` (~50), `dev_test_group.py` (~30), `index_pools.py` (~30), `virtualmachinepolicies.py` (~40), others (~200)

### Phase 5: Subsystem Modules (~60 modules, ~2,000 new tests)

| Directory | Files | New tests |
|-----------|-------|-----------|
| `activateapps/` | 8 | ~500 |
| `datacube/` | 5 | ~200 |
| `deployment/` | 5 | ~200 |
| `drorchestration/` | 8 | ~350 |
| `cleanroom/` | 5 | ~150 |
| `policies/` (config, schedule) | 3 | ~300 |
| `clouddiscovery/`, `dashboard/`, `monitoringapps/`, `securitycenter/`, `clients/`, `exchange/`, `reports/` | ~20 | ~300 |

### Phase 6: Constants, Init, and Edge Cases (~20 modules, ~300 new tests)

- All `constants.py` files — test enum completeness, dict key coverage
- `cvpysdk.py` — deeper `make_request` edge cases (token renewal on 401, SSL errors, timeouts)
- `services.py` — every endpoint template resolves correctly
- `exception.py` — all module/id combinations produce correct messages
- `__init__.py` files with dynamic import logic

## Testing Strategy by Code Pattern

**Property getters** (31% of code): Set `self._attr` via `make_entity`, assert property returns it. For setters, assert they call `update_properties()`.

**API-calling methods** (40% of code): 3-4 tests per method:
1. Success — mock `make_request` → `(True, good_response)`, assert return value
2. API failure — mock → `(False, error_response)`, assert `SDKException`
3. Empty/malformed response — mock → `(True, empty_response)`, assert `SDKException`
4. Bad input type — pass wrong type, assert `SDKException`

**JSON construction** (20% of code): Call method with known inputs, assert specific keys/values in returned dict. Test optional params present/absent.

**Error handling** (5% of code): Verify correct exception module and error ID in raised `SDKException`.

## Totals

| | Current | Target | Delta |
|---|---------|--------|-------|
| Coverage | 28% | 100% | +72% |
| Statements covered | 14,472 | 52,271 | +37,799 |
| Tests | 1,939 | ~14,900 | ~12,960 |
| Test files | 268 | 268 (enhanced, no new files) | 0 |
| Est. run time | 3.5s | ~25-30s | All mock-based |

## Verification

After each phase:
1. `uv run pytest tests/unit/ --cov=cvpysdk --cov-report=term-missing` — check coverage %
2. `uv run pytest tests/unit/ -v --tb=short` — confirm all tests pass
3. `ruff check .` — confirm no lint issues

Target coverage milestones:
- After Phase 1: ~55%
- After Phase 2: ~70%
- After Phase 3: ~82%
- After Phase 4: ~90%
- After Phase 5: ~97%
- After Phase 6: 100%
