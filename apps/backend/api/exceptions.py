class RecordNotFound(Exception):
    def __init__(self, cls_name: str, detail: str = None):
        if detail is None:
            detail = f"{cls_name}: Record not found"
        super().__init__(detail)
        self.detail = detail


class MultipleRecordsFound(Exception):
    def __init__(self, cls_name: str, detail: str = None):
        if detail is None:
            detail = f"{cls_name}: Multiple records found, expected one"
        super().__init__(detail)
        self.detail = detail


class DuplicateRecordError(Exception):
    def __init__(self, cls_name: str, field: str = None, detail: str = None):
        if detail is None:
            if field:
                detail = f"{cls_name}: A record with the same '{field}' field already exists"
            else:
                detail = f"{cls_name}: A record with the given values already exists"
        super().__init__(detail)
        self.detail = detail


class MissingFieldsError(Exception):
    def __init__(self, cls_name: str, field: str = None, detail: str = None):
        if detail is None:
            if field:
                detail = f"{cls_name}: Required field '{field}' is missing"
            else:
                detail = f"{cls_name}: Required fields are missing"
        super().__init__(detail)
        self.detail = detail
