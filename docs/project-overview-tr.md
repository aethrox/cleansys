### cleansys Proje Özeti (TR)

**cleansys**, dosya sistemindeki dijital “çöplüğü” (eski, büyük, gereksiz dosyalar) tespit edip temizlemeyi kolaylaştıran minimalist bir **komut satırı aracı (CLI)**’dır. Tamamen yerel çalışır, kullanıcıdan açık onay almadan hiçbir yıkıcı işlem yapmaz ve davranışı yalnızca komut satırı argümanlarıyla kontrol edilir.

---

### Kullanılan Teknolojiler ve Araçlar

- **Dil**: Python 3.8+
- **CLI Framework**: Click veya Typer (tek bir CLI kütüphanesi, minimum bağımlılık)
- **Dosya İşlemleri (standart kütüphane)**:
  - `pathlib` / `os`: Dizin gezme, dosya bilgisi toplama
  - `datetime`: “Kaç gündür kullanılmadı?” hesabı
  - `shutil`: Dosya taşıma (move)
  - `zipfile`: Arşiv (zip) oluşturma
- **Paketleme & Dağıtım**:
  - `pyproject.toml` ve `requirements.txt` ile paket yapısı
  - `cleansys` komutu ile global CLI olarak çalıştırılabilir
- **Testler**: `tests/` klasörü (pytest tarzı birim testler)
- **Demo & Dokümantasyon**:
  - `cli-example.gif` + `demo.tape` (VHS ile otomatik CLI demosu)
  - `docs/*.md` (techstack, userflow, scope vb.)

---

### Mimari: Modüllerin Sorumlulukları

`src/` altında her dosyanın tek ve net bir sorumluluğu vardır:

- **`scanner.py`**:
  - Verilen kök dizinden itibaren dosyaları gezer.
  - Boyut, son erişim tarihi, uzantı gibi ham metadata çıkarır.
  - Symlink’leri takip etmez, sistem/hidden dosyalardan kaçınır (güvenlik ve sadelik için).

- **`analyzer.py`**:
  - `scanner`’dan gelen dosya listesini alır.
  - `--unused-days`, `--min-size`, `--file-type` gibi kriterlere göre filtreler.
  - Sadece “ilgileneceğimiz” dosyaları döner (`FileInfo` kayıtları).

- **`interface.py`**:
  - Terminalde dosya bilgilerini gösterir (boyut, son erişim tarihi, index vb.).
  - Kullanıcıdan aksiyon alır: Keep / Move / Archive / Delete / Skip.
  - Koşu sonunda özet (summary) ekranını basar.

- **`operations.py`**:
  - Gerçek dosya işlemlerini yapar: move, archive, delete.
  - Hata yakalama (PermissionError, FileNotFoundError vb.), loglama ve dry-run davranışlarını içerir.
  - Kullanıcıyla direkt etkileşime girmez; sadece kendisine verilen işi uygular.

- **`size_parser.py`**:
  - `10MB`, `500KB` gibi metinleri bayt cinsinden sayıya çevirir.
  - CLI’den gelen `--min-size` gibi parametreler için kullanılır.

- **`main.py`**:
  - CLI argümanlarını (root path, `unused_days`, `min_size`, `file_type`, `dry_run`) parse eder.
  - `scanner → analyzer → interface → operations` hattını kurar ve orkestrasyonu yapar.

---

### Algoritma Akışı (Yüksek Seviye)

1. **Girdi**  
   Kullanıcı örneğin şu komutu çalıştırır:

   ```bash
   cleansys ~/Downloads --unused-days 180 --min-size 50MB --file-type .log --dry-run
   ```

2. **Tarama (`scanner`)**  
   - `pathlib.Path(root).rglob("*")` benzeri bir mantıkla kök dizin gezinir.
   - Her dosya için:
     - Boyut (`stat().st_size`)
     - Son erişim zamanı
     - Uzantı / isim gibi bilgiler okunur.
   - Hata (izin yok, bozuk link vb.) durumunda:
     - Dosya atlanır, log’a uyarı yazılır; program çökmez.

3. **Analiz / Filtreleme (`analyzer`)**  
   - Her dosya için:
     - `unused_days` kriteri: bugün − son erişim ≥ parametredeki gün.
     - `min_size` kriteri: boyut ≥ `min_size_bytes`.
     - `file_type` kriteri: uzantı eşleşmesi.
   - Tüm kriterleri sağlayan dosyalar “eşleşenler listesi”ne alınır.

4. **Kullanıcı ile Etkileşim (`interface`)**  
   - Örneğin 47 dosya bulunduysa önce kısa bir özet gösterilir:
     - “47 dosya bulundu, toplam 892 MB”.
   - Sonra her dosya için:
     - `index/total`, boyut, son erişim tarihi, tip gibi bilgiler.
     - Aksiyon menüsü: `[K]eep | [M]ove | [A]rchive | [D]elete | [S]kip all`.
   - Kullanıcı her dosyada bir tuşa basar:
     - `K`: dosya üzerinde işlem yapılmaz (tut).
     - `M`: hedef klasör sorulur → `operations.move_file`.
     - `A`: arşiv adı/hedefi belirlenir → `operations.archive_files`.
     - `D`: dosya bilgisi tekrar gösterilir ve **“yes/y” onayı alınmadan** `delete_file` çağrılmaz.
     - `S`: kalan dosyaları “skip” olarak işaretler (ya da batch moduna göre davranır).

5. **Dosya İşlemleri (`operations`)**  
   - `--dry-run` aktifse:
     - Gerçek dosya işlemi yapılmaz.
     - “[DRY RUN] Would delete: ...” gibi mesajlar ve log satırları yazılır.
   - Normal modda:
     - `move_file`: `shutil.move` ile taşıma; hata olursa log + `False` döner.
     - `archive_files`: `zipfile.ZipFile` ile dosyaları zip’e ekleyerek arşiv oluşturur.
     - `delete_file`: `Path.unlink()` veya eşdeğer çağrılarla silme işlemi yapar.
   - Her işlem için:
     - Log dosyasına satır eklenir: zaman damgası, aksiyon tipi (MOVE / ARCHIVE / DELETE), yol ve boyut bilgisi.
     - Hata varsa `[ERROR]` veya `[WARN]` prefiksiyle kaydedilir.

6. **Özet ve Sonuç (`interface.show_summary`)**  
   - Koşu sonunda şu bilgiler özetlenir:
     - Kaç dosya tutuldu.
     - Kaç dosya taşındı ve nereye.
     - Kaç dosya arşivlendi ve arşiv adı.
     - Kaç dosya silindi, yaklaşık ne kadar yer açıldı.
   - Hatalar varsa “şu kadar dosya atlandı / şu hatalar görüldü” şeklinde raporlanır.

---

### A’dan Z’ye Geliştirme Süreci (Mantıksal)

1. **Problem Tanımı & Kapsam**  
   - Amaç: Downloads/Desktop gibi klasörlerde biriken gereksiz dosyaları, kullanıcıya adım adım sorarak güvenli şekilde temizlemek.
   - Çerçeve:
     - Sadece yerel dosya sistemi.
     - Sadece metadata (tarih, boyut, uzantı).
     - Otomatik silme yok; her zaman kullanıcı onayı.

2. **Teknoloji ve Mimari Kararları**  
   - Python 3.8+ ve standart kütüphane odaklı yaklaşım.
   - GUI yerine basit ve taşınabilir bir CLI.
   - Modül bazlı sorumluluk ayrımı: `scanner`, `analyzer`, `interface`, `operations`, `size_parser`, `main`.
   - Harici bağımlılıkları minimumda tutma (tek CLI framework).

3. **Proje İskeleti**  
   - `src/` ve `tests/` dizinlerinin oluşturulması.
   - Her modülde fonksiyon imzalarının belirlenmesi (scan, filter, display, move, archive, delete).
   - `main.py` içinde basit bir CLI giriş noktası hazırlanması.

4. **Scanner + Analyzer Uygulaması**  
   - Önce yalnızca dizini gezip dosya listesi çıkaran bir `scanner`.
   - Sonra en temel kriter olan `--unused-days` ile filtreleme.
   - Ardından `--min-size` ve `--file-type` kriterlerinin eklenmesi.
   - Bu aşamada `test_scanner.py` ve `test_analyzer.py` ile birim testlerin yazılması.

5. **CLI ve Interface Olgunlaştırılması**  
   - `main.py` içerisinde Click/Typer ile argüman ve opsiyonların tanımlanması.
   - `interface.py` ile:
     - Dosya başına gözükecek alanların karar verilmesi.
     - Kullanıcı aksiyon menüsünün tasarlanması.
     - Hatalı girişlerde ne olacağının belirlenmesi.
   - `docs/userflow.md` ile bu akışın belgelenmesi veya bu dokümana göre geliştirme yapılması.

6. **Operations ve Güvenlik Kuralları**  
   - Başlangıçta her şeyin dry-run olarak çalışması (gerçek silme yok).
   - Sonrasında:
     - Move, archive ve delete fonksiyonlarının eklenmesi.
     - Tüm yıkıcı işlemlerden önce dosya bilgisini gösterip “emin misin?” onayının alınması.
   - Log formatının belirlenip uygulanması.

7. **Testlerin Genişletilmesi**  
   - Tüm modüller için unit test’lerin eklenmesi:
     - Farklı kriter kombinasyonları.
     - Hata senaryoları.
     - Dry-run ve gerçek koşu senaryoları.
   - Gerçek kullanıcı dosyalarına dokunmayan geçici dizin tabanlı testler.

8. **Demo ve Dokümantasyon**  
   - `cli-example.gif` için:
     - Küçük demo dosyaları oluşturan bir script.
     - `demo.tape` ile VHS üzerinden terminal etkileşimi kaydedilip GIF’e dönüştürülmesi.
   - `README.md`, `docs/techstack.md`, `docs/scope.md` vb. ile:
     - Ne işe yaradığı.
     - Nasıl kullanıldığı.
     - Hangi kısıtların olduğu.
     - Hangi teknoloji ve mimari tercih edildiği.

9. **Paketleme ve Yayınlama**  
   - `pyproject.toml` ve `cleansys.egg-info` ile Python paketi haline getirme.
   - `pip install .` ile yerel kurulumun test edilmesi.
   - `cleansys` komutunun PATH üzerinden çağrılabildiğinin doğrulanması.

---

### Kısa Özet

- **Algoritma**: Dizini tara → kriterlere göre filtrele → kullanıcıya her dosyayı açıkça göster → kullanıcı aksiyon seçsin → dry-run veya gerçek işlem → logla → özetle.
- **Mimari**: Her modül tek bir iş yapar; tarama, analiz, arayüz ve operasyonlar birbirinden ayrıdır.
- **Araçlar**: Python + küçük bir CLI kütüphanesi + standart kütüphane; üzerine testler, demo GIF ve markdown dokümantasyon.


