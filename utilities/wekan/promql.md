
```
sum by (board_title) (
  wekan_cards{
    status="active",
    board_title=~"home|work",
  }
)
```

```
sum(
  wekan_cards{
    status="active",
    board_title=~"home|work",
  }
)
```