class ExportError(Exception):
    pass

class ExportValidationError(ExportError):
    pass

class ExportRenderError(ExportError):
    pass

class ExportStorageError(ExportError):
    pass
