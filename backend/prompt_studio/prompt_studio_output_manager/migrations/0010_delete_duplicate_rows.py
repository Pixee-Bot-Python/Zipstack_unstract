# Generated by Django 4.2.1 on 2024-03-22 11:19

from django.db import migrations, models


def delete_duplicates_and_nulls(apps, schema_editor):
    prompt_studio_output_manager = apps.get_model(
        "prompt_studio_output_manager", "PromptStudioOutputManager")

    # Delete rows where prompt_id, document_manager, profile_manager, or tool_id is NULL
    prompt_studio_output_manager.objects.filter(
        models.Q(prompt_id=None) |
        models.Q(document_manager=None) |
        models.Q(profile_manager=None) |
        models.Q(tool_id=None)
    ).delete()

    # Find duplicate rows based on unique constraint fields and count their occurrences
    duplicates = prompt_studio_output_manager.objects.values(
        'prompt_id', 'document_manager', 'profile_manager', 'tool_id'
    ).annotate(
        count=models.Count('prompt_output_id')
    ).filter(
        count__gt=1  # Filter to only get rows that have duplicates
    )

    # Iterate over each set of duplicates found
    for duplicate in duplicates:
        # Find all instances of duplicates for the current set
        pks = prompt_studio_output_manager.objects.filter(
            prompt_id=duplicate['prompt_id'],
            document_manager=duplicate['document_manager'],
            profile_manager=duplicate['profile_manager'],
            tool_id=duplicate['tool_id']
        ).order_by('-created_at').values_list('pk')[1:]  # Order by created_at descending and skip the first one (keep the latest)

        # Delete the duplicate rows
        prompt_studio_output_manager.objects.filter(pk__in=pks).delete()


class Migration(migrations.Migration):
    dependencies = [
        (
            "prompt_studio_output_manager",
            "0009_remove_promptstudiooutputmanager_doc_name_and_more",
        ),
    ]

    operations = [
        migrations.RunPython(delete_duplicates_and_nulls,
                             reverse_code=migrations.RunPython.noop),
    ]