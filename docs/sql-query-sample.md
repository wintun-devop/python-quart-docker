### Upsert Query
```
INSERT INTO esm_inventory (
    id,
    name,
    model_no,
    price,
    qty,
    created_at,
    updated_at
)
VALUES ('p001', 'router-a', 'model-roter-a', 33.3,30,'2025-09-06 18:03:36.17129','2025-09-06 18:03:36.17129')
ON CONFLICT ON CONSTRAINT esm_inventory_model_no_key DO UPDATE
SET
    name=EXCLUDED.name,
    model_no=EXCLUDED.model_no,
    price=EXCLUDED.price,
    qty=EXCLUDED.qty,
    created_at=EXCLUDED.created_at,
    updated_at=EXCLUDED.updated_at;
```