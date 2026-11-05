# هندسة عكسية: Dragon Mania (أندرويد، Gameloft 2014)

أدوات Python لفك ملفات اللعبة. الأدوات بس في المستودع، وملف الـ APK والملفات المستخرجة ما تنرفع.

## معلومات اللعبة

| البند | القيمة |
|---|---|
| الحزمة | `com.gameloft.android.ANMP.GloftPDHM` (الاسم الداخلي: PocketDragon) |
| الإصدار | 4.0.0 (2014) |
| المحرك | GLLib من Gameloft بلغة **Java** (منطق اللعبة كله في `classes.dex`، 989 كلاس مشفّرة الأسماء) |
| المكتبات الأصلية | `libgenerator.so` و `libnativeU.so` (صغيرة) |
| الإعلانات والخدمات | Tapjoy، Facebook، GCM Push، Weibo |
| الدقة | نسختين من الموارد: `assets/800x480` و `assets/480x320` |

## صيغة الحزم (Packs)

الملفات المرقّمة في `assets/800x480` (0، 1، 2...) هي حزم بالشكل:

```
u16 count
u32 offset[count]      // بداية كل عنصر، والأخير ينتهي بنهاية الملف
entry = u8 flag + payload
```

الحزم الكبيرة مقسّمة على ملفات حجمها 2,000,000 بايت (`5` ثم `5.1` ثم `5.2`)، تنضم ورا بعض.

| الحزمة | المحتوى |
|---|---|
| 2، 5، 8، 9، 12 | صور BSprite (حوالي 967 صورة). **12** = أجزاء التنانين، **5** = الواجهة والخلفيات |
| 3 | 91 صوت OGG |
| EN و AR و FR... | جداول النصوص لكل لغة |
| 4، 6، 7، 10، 13، 14، 16 | بيانات اللعبة (خرائط، تأثيرات، جداول توازن). لسا ما انفكّت |

## صيغة BSprite (الإصدار 0x05DF)

```
u16 0x05DF, u32 flags, modules / frames / anims ...
u16 pixel_format   (0x8888 | 0x4444 | 0x1555 | 0x0565)
u16 encoding
u8  n_images
  لكل صورة:  u8 n_palettes, u8 n_colors, palettes[n_palettes][n_colors]
  لكل صورة:  u16 w, u16 h, u32 size, data[size]
```

الترميزات اللي انفكّت:

- `0x27F1` I127RLE: البايت > 127 يعني تكرار (c-128) مرة للون اللي بعده، وغيره بكسل واحد.
- `0x56F2` I256RLE: البايت > 127 يعني (c-128) بكسل حرفي ياي بعده، وغيره تكرار c مرة.
- `0x64F0` I64RLE: البتات الدنيا رقم اللون (log2 لعدد الألوان) والعليا عدد التكرار ناقص 1.
- `0xA127 / 0xA256 / 0xA640`: نفس اللي فوق، وبعدها قناة شفافية (Alpha) مضغوطة بـ `FE n v`.

كل صورة فيها عدة لوحات ألوان (palettes)، وهي ألوان التنين المختلفة. الأداة تصدّر كل لوحة كصورة PNG مستقلة.

## الاستخدام

```bash
unzip game.apk -d apk
python3 tools/export.py         apk/assets/800x480 out      # الصور -> out/sprites
python3 tools/extract_sounds.py apk/assets/800x480 out/sounds
python3 tools/texts.py          apk/assets/800x480 EN out/texts_EN.json
python3 tools/dex.py            apk/classes.dex out         # نصوص وأسماء الكلاسات
```

تحتاج Python 3 بس، بدون مكتبات إضافية.
