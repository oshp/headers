function crash_report(){
  Raven.showReportDialog({
    eventId: '{{ event_id }}',
    dsn: '{{ public_dsn }}'
  });
}
