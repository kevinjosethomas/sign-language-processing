import CheckIcon from "@mui/icons-material/Check";

export default function Checkbox({ label }: { label: string }) {
  return (
    <div className="flex items-center justify-end gap-2">
      <div className="w-5 h-5 bg-blue-600 flex items-center justify-center rounded text-sm text-white">
        <CheckIcon color="inherit" fontSize="inherit" />
      </div>
      <p className="text-white text-lg">{label}</p>
    </div>
  );
}
