@echo off

python C:\Programme\Python24\Scripts\i18ndude rebuild-pot --pot i18n\eduComponents.pot .
python C:\Programme\Python24\Scripts\i18ndude merge --pot i18n\eduComponents.pot --merge i18n\schemas.pot
python C:\Programme\Python24\Scripts\i18ndude merge --pot i18n\eduComponents.pot --merge i18n\other.pot
python C:\Programme\Python24\Scripts\i18ndude sync --pot i18n\eduComponents.pot i18n\eduComponents-de.po
