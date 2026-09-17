# Quy trình làm việc, log và Git cho DocAI

Áp dụng cho toàn bộ repository **DocAI Document Intelligence Platform**, bao gồm bốn vùng responsibility (Track A, Track B, Product Engineering và Research & Evaluation), phần dùng chung và AI hỗ trợ dự án.

Mục tiêu của quy trình này là giữ repository gọn, mọi thay đổi đều truy được lý do, không có nhiều file cùng chức năng, không biến notebook thành nơi chứa toàn bộ logic, và không tuyên bố một chức năng đã hoàn thành khi mới chỉ có scaffold hoặc kiểm tra tĩnh.

---

## 1. Một task hoàn chỉnh là gì?

Trước khi bắt đầu một task, phải xác định ngắn gọn:

- **Mục tiêu:** task này giải quyết đúng vấn đề gì?
- **Owner:** Nhánh A, Nhánh B hay A + B?
- **Input:** đọc file, data, schema hoặc output nào?
- **Output canonical:** kết quả chính thức sẽ nằm ở đâu?
- **Phạm vi được phép sửa:** những file/folder nào có thể thay đổi?
- **Phạm vi không được sửa:** những phần nào phải giữ nguyên?
- **Kiểm tra cần chạy:** compile, test, notebook validation, schema validation, YAML validation hay kiểm tra khác?
- **Điều kiện PASS:** thế nào mới được coi là hoàn thành?
- **Điều kiện STOP/BLOCKED:** khi nào phải dừng thay vì tự suy đoán hoặc viết tiếp?

Một task nên tạo ra **một kết quả kỹ thuật rõ ràng**.

Không nên gộp nhiều việc lớn không liên quan vào cùng một prompt, ví dụ:

```text
audit repo + tải dataset + train model + benchmark + làm dashboard + deploy
```

Thay vào đó, tách thành các task có đầu ra và điều kiện kiểm tra riêng.

Khi giao task cho AI, prompt phải nói rõ:

```text
đọc gì
→ làm gì
→ được sửa ở đâu
→ không được sửa gì
→ output canonical ở đâu
→ validation nào phải chạy
→ khi nào PASS
→ khi nào phải STOP
```

Sau khi task hoàn tất:

1. Kiểm tra file/folder có đúng vị trí không.
2. Kiểm tra có tạo file trùng chức năng với file cũ không.
3. Nếu một file mới thay thế file cũ, phải cập nhật/xóa file cũ trong cùng thay đổi nếu an toàn.
4. Chạy validation phù hợp.
5. Cập nhật `log/progress-log.md`.
6. Kiểm tra `git diff` và `git status`.
7. Commit đúng nhóm file của task.

---

## 2. Source of truth và output canonical

Repository phải luôn cố gắng có **một nguồn sự thật chính** cho mỗi loại thông tin.

Ví dụ:

- Phân công Nhánh A/B: `docs/specs/task-split.md`
- Nhật ký tiến độ chung: `log/progress-log.md`
- Schema output chung: package schema canonical trong `src/docai/`
- Mã nguồn chính: `src/docai/`
- Script thực thi: `scripts/`
- Notebook khám phá/phân tích: `notebooks/`
- Tài liệu kỹ thuật: `docs/`
- Dữ liệu gốc: `data/raw/`
- Dữ liệu trung gian: `data/interim/`
- Dữ liệu đã xử lý: `data/processed/`

Không tạo các file kiểu:

```text
task-split-copy.md
task-split-final.md
task-split-final2.md
schema-new.py
benchmark-latest.py
report-new.md
```

nếu đã có file canonical cùng vai trò.

Nếu cần đổi tên hoặc thay thế file canonical, phải cập nhật consumer và documentation liên quan trong cùng task.

---

## 3. Quy tắc cho `src/`, `scripts/` và `notebooks/`

### 3.1 `src/docai/` là nơi chứa implementation chính

Logic có thể tái sử dụng phải nằm trong:

```text
src/docai/
```

Ví dụ:

- data loading;
- preprocessing;
- OCR/KIE/VLM wrappers;
- schema;
- fraud rules;
- explainability;
- evaluation;
- FastAPI logic;
- Plotly Dash logic.

Không copy cùng một implementation sang nhiều nơi.

### 3.2 `scripts/` chỉ là entry point

Các file trong:

```text
scripts/
```

chỉ nên làm các việc như:

```text
đọc argument/config
→ gọi function trong package docai
→ ghi hoặc hiển thị output
```

Không đặt business logic lớn trực tiếp trong `scripts/`.

### 3.3 `notebooks/` là nơi khám phá, không phải source code chính

Notebook `.ipynb` được dùng để:

- EDA;
- thử nghiệm;
- visualization;
- giải thích kết quả;
- gọi các function từ `src/docai/`.

Notebook không nên là nơi duy nhất chứa:

- loader;
- preprocessing;
- metric;
- model wrapper;
- reusable utility;
- pipeline chính.

Nguyên tắc:

```text
notebook
   ↓ gọi
src/docai/
```

không phải:

```text
notebook
   ↓
chứa toàn bộ project
```

Nếu một đoạn code trong notebook bắt đầu được dùng lại ở nhiều nơi, phải cân nhắc chuyển nó sang `.py`.

---

## 4. Quy tắc cho Nhánh A và Nhánh B

Repository có hai processing backend chính bên trong một product:

- **Nhánh A:** pipeline cổ điển/modular.
- **Nhánh B:** pipeline dựa trên VLM.
- **A + B:** phần dùng chung như schema, Product integration, evaluation, documentation hoặc benchmark.

Mọi task phải ghi rõ owner là:

```text
A
B
A + B
```

Không được gán một task dùng chung cho riêng A hoặc B nếu thực tế cả hai pipeline đều phụ thuộc vào nó.

Hai track được phép khác cách xử lý, nhưng output phải đi về contract/schema chung khi được dùng trong Product hoặc Research comparison.

Không duplicate schema chỉ vì hai track khác implementation.

---

## 5. Log tiến độ bắt buộc

Nhật ký canonical của repository là:

```text
log/progress-log.md
```

Không tạo thêm log riêng kiểu:

```text
log_a.md
log_b.md
progress-final.md
progress-new.md
```

trừ khi architecture sau này có quyết định chính thức khác.

Mỗi entry nên đủ ngắn để đọc nhanh nhưng phải trả lời được:

- thời gian;
- loại task hoặc phase;
- owner A/B/A+B;
- việc đã làm;
- file/output chính;
- trạng thái;
- validation đã chạy;
- đúng một next step hoặc blocker nếu còn.

Không ghi:

- raw console log dài;
- secret/token;
- credential;
- dữ liệu nhạy cảm;
- toàn bộ stack trace nếu không cần thiết.

Chi tiết kỹ thuật nên nằm trong source, notebook, report hoặc docs tương ứng.

Không ghi timestamp tương lai.

Không sửa lịch sử log chỉ để làm báo cáo trông đẹp. Nếu buộc phải hiệu chỉnh một entry sai, phải để lại dấu vết rõ ràng về việc hiệu chỉnh.

---

## 6. Kỷ luật file và artifact

Trước khi tạo file mới:

1. Tìm xem đã có file cùng vai trò chưa.
2. Nếu có, ưu tiên **update in place**.
3. Chỉ tạo file mới nếu nó có trách nhiệm rõ ràng và khác file cũ.
4. Không tạo folder trống để “dành cho tương lai”.

Không dùng tên mơ hồ như:

```text
final2
new
latest
copy
backup
test_ok
```

Artifact lớn thuộc các thư mục như:

```text
data/
models/
artifacts/
```

theo `.gitignore` và quy ước hiện hành.

Repository chỉ nên giữ:

- source code;
- config;
- schema/contract;
- manifest;
- report nhỏ;
- notebook cần thiết;
- tài liệu tái tạo kết quả.

Không commit dataset lớn hoặc model weight nếu quy định repository không cho phép.

---

## 7. Quy tắc về scaffold, TODO và code chưa triển khai

Các từ như:

```text
TODO
FIXME
NotImplementedError
pass
placeholder
mock
dummy
```

không tự động đồng nghĩa với lỗi.

Phải phân biệt:

### Hợp lệ

Chức năng thuộc phase sau và file hiện chỉ cần scaffold.

### Cần sửa

Task hiện tại đáng lẽ phải triển khai chức năng đó nhưng vẫn còn placeholder.

### Nguy hiểm

Placeholder hoặc mock có thể bị hiểu nhầm thành output thật.

Không viết fake implementation chỉ để làm validation xanh.

Ví dụ không được tạo:

```python
def run_model():
    return {"status": "success"}
```

nếu model thực tế chưa chạy.

Phải nói đúng trạng thái:

```text
scaffold
chưa triển khai
đã triển khai
đã static-check
đã runtime-test
```

Các trạng thái này không được đánh đồng với nhau.

---

## 8. Dữ liệu, metric và kết quả thực nghiệm

Không bịa:

- dataset statistics;
- accuracy;
- precision;
- recall;
- F1;
- IoU;
- latency;
- cost;
- benchmark result;
- model output.

Nếu cần số để minh họa trong tài liệu, phải ghi rõ:

> Ví dụ minh họa, không phải kết quả thực nghiệm của repository.

Khi chưa có data/model output thật, report phải nói rõ:

```text
CHƯA CÓ KẾT QUẢ THỰC NGHIỆM
```

thay vì tạo placeholder có vẻ giống kết quả thật.

---

## 9. Plotly Dash, không Power BI

Dashboard chính thức của project sử dụng:

```text
Python
→ pandas
→ Plotly
→ Dash
```

Không sử dụng Power BI trong architecture hiện hành.

Không thêm:

- `.pbix`;
- DAX;
- Power Query;
- dependency hoặc hướng dẫn Power BI.

Nếu dashboard chưa tới phase triển khai, chỉ giữ scaffold/architecture cần thiết.

Không tự tạo dashboard hoàn chỉnh trong một task audit hoặc refactor.

---

## 10. Git: branch → kiểm tra → commit → push → PR

Không commit trực tiếp vào `main`.

Dùng branch phù hợp với task, ví dụ:

```text
feat/track-a-ocr
feat/track-b-vlm
feat/data-eda
refactor/src-layout
docs/concepts
fix/schema-imports
```

Tên branch chỉ là gợi ý; nếu repository đã có quy ước khác thì ưu tiên quy ước hiện hành.

Trước task mới:

```bash
git checkout main
git pull origin main
git checkout <branch>
```

Nếu branch đã tồn tại, cập nhật nó từ `main` theo workflow mà nhóm đang dùng.

Nếu đang có code dở và cần đồng bộ:

```bash
git stash
git checkout main
git pull origin main
git checkout <branch>
git merge main
git stash pop
```

Nếu có conflict:

```text
đọc conflict
→ sửa bằng tay
→ chạy validation lại
→ commit
```

Không giải conflict bằng cách chọn bừa một phía.

---

## 11. Stage và commit theo từng nhóm công việc

Trước commit:

```bash
git status
git diff
```

Stage từng file cụ thể:

```bash
git add <file-1> <file-2> ...
```

Không mặc định dùng:

```bash
git add .
git add -A
```

nếu chưa kiểm tra toàn bộ file thay đổi.

Commit message nên mô tả đúng task:

```text
feat(data): add reusable EDA loaders
refactor(core): move schema into docai package
docs(concepts): explain Track A pipeline
fix(api): update imports after src migration
```

Không gộp code, docs, dataset lớn và thay đổi không liên quan vào cùng một commit nếu có thể tách hợp lý.

---

## 12. Validation trước khi commit

Chỉ chạy những validation phù hợp với task.

Ví dụ sau khi sửa Python:

```bash
python -m compileall src scripts
```

Nếu project hỗ trợ editable install:

```bash
pip install -e .
python -c "import docai"
```

Nếu có test phù hợp:

```bash
pytest
```

Nếu sửa notebook:

- kiểm tra file `.ipynb` vẫn là JSON hợp lệ;
- không để notebook chứa output khổng lồ không cần thiết;
- kiểm tra import từ package `docai` vẫn hoạt động khi môi trường đã cài đúng.

Nếu sửa YAML:

- parse/validate YAML.

Nếu sửa schema hoặc contract dùng chung:

- kiểm tra các consumer quan trọng;
- cần review chéo trước merge nếu thay đổi có thể ảnh hưởng cả A và B.

`compile PASS` không đồng nghĩa với:

```text
runtime PASS
model PASS
pipeline PASS
benchmark PASS
```

Báo cáo phải nói đúng loại kiểm tra đã thực hiện.

---

## 13. Review trước merge

Trước khi tạo PR vào `main`, kiểm tra:

- Scope commit có đúng task không?
- Có file thừa không?
- Có dataset/model binary bị add nhầm không?
- Có file duplicate cùng chức năng không?
- Canonical path có bị thay đổi mà consumer chưa cập nhật không?
- Import path có còn đường dẫn cũ không?
- Documentation có còn mô tả architecture cũ không?
- `log/progress-log.md` đã được cập nhật chưa?
- Validation liên quan đã chạy chưa?
- Blocker còn lại có được ghi rõ không?
- Có số liệu/metric nào chưa có bằng chứng nhưng bị viết như kết quả thật không?
- Có scaffold nào bị mô tả sai thành implementation hoàn chỉnh không?

Nếu thay đổi ảnh hưởng schema, output contract hoặc phần dùng chung của A/B, phải review kỹ hơn trước merge.

---

## 14. Quy tắc khi dùng AI trong repository

AI phải đọc context liên quan trước khi sửa.

Không được:

- tự thêm công nghệ chỉ vì “best practice”;
- tự đổi stack lớn;
- tự tải dataset;
- tự gọi API mất phí;
- tự train model;
- tự tạo metric;
- tự tạo hàng loạt file rỗng;
- tự over-engineer architecture;
- tự tuyên bố `100% hoàn thành` khi chỉ mới static-check.

Nếu task chỉ là audit:

```text
audit
→ phát hiện vấn đề
→ sửa nhỏ nếu được phép
→ report
```

không biến thành:

```text
audit
→ refactor toàn repo
→ triển khai model
→ tạo dashboard
→ deploy
```

Nếu cần implementation lớn ngoài scope, ghi:

```text
CHƯA TRIỂN KHAI — thuộc phase sau
```

thay vì tự mở rộng task.

---

## 15. Quy tắc cho tài liệu kỹ thuật

Tài liệu trong `docs/` phải:

- dùng tiếng Việt có dấu UTF-8;
- giữ nguyên thuật ngữ English quan trọng khi cần;
- không mô tả kế hoạch như thể đã triển khai;
- không ghi metric giả;
- không lặp cùng nội dung ở nhiều file;
- link về file canonical thay vì copy nguyên một contract.

Với tài liệu giải thích thuật toán/model/kỹ thuật, tuân thủ:

```text
docs/concepts/explanation-style.md
```

nếu file này tồn tại.

---

## 16. Khi nào một task được coi là hoàn thành?

Một task chỉ được đánh dấu `Done` khi:

```text
mục tiêu rõ
+
output canonical đúng vị trí
+
không duplicate
+
validation phù hợp đã chạy
+
log đã cập nhật
+
không còn blocker thuộc scope của task
```

Nếu chỉ hoàn thành một phần, dùng trạng thái phù hợp như:

```text
In Progress
Blocked
Scaffold Ready
Static Check Passed
```

thay vì `Done`.

Nguyên tắc cuối cùng:

> Repository nên ưu tiên ít file hơn nhưng rõ trách nhiệm, ít code hơn nhưng đúng scope, và mọi kết luận kỹ thuật phải có bằng chứng tương ứng.
