# Update the homepage only after a successful compilation, including IDE builds.
use Cwd qw(abs_path);
use File::Basename qw(dirname);
my $cv_root = dirname(abs_path(__FILE__));
$pdf_mode = 1;
$success_cmd = 'python3 "' . $cv_root . '/../scripts/build_cv.py" --sync %D';
