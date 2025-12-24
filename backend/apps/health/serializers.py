from rest_framework import serializers
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Vaccination, HealthRecord
from apps.pets.serializers import PetListSerializer


class VaccinationSerializer(serializers.ModelSerializer):
    """
    Serializer for Vaccination model with full validation.
    """
    pet_name = serializers.CharField(source='pet.name', read_only=True)
    pet_id = serializers.IntegerField(source='pet.id', read_only=True)
    veterinarian_name = serializers.CharField(
        source='veterinarian.get_full_name',
        read_only=True
    )

    class Meta:
        model = Vaccination
        fields = [
            'id',
            'pet',
            'pet_id',
            'pet_name',
            'vaccine_name',
            'due_date',
            'status',
            'administered_date',
            'veterinarian',
            'veterinarian_name',
            'batch_number',
            'notes',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'pet_id', 'pet_name', 'veterinarian_name']

    def validate_vaccine_name(self, value):
        """
        Validate vaccine name is not empty.
        """
        if not value or not value.strip():
            raise serializers.ValidationError('Vaccine name cannot be empty.')
        return value.strip()

    def validate_due_date(self, value):
        """
        Validate due date is not in the past for new vaccinations.
        """
        if self.instance is None and value < timezone.now().date():
            raise serializers.ValidationError(
                'Due date cannot be in the past for new vaccinations.'
            )
        return value

    def validate(self, attrs):
        """
        Cross-field validation.
        """
        administered_date = attrs.get('administered_date') or (
            self.instance.administered_date if self.instance else None
        )
        due_date = attrs.get('due_date') or (
            self.instance.due_date if self.instance else None
        )
        status = attrs.get('status') or (
            self.instance.status if self.instance else 'pending'
        )

        if administered_date:
            if administered_date > timezone.now().date():
                raise serializers.ValidationError({
                    'administered_date': 'Administered date cannot be in the future.'
                })
            
            if due_date and administered_date < due_date:
                raise serializers.ValidationError({
                    'administered_date': 'Administered date cannot be before due date.'
                })

        if status == 'completed' and not administered_date:
            raise serializers.ValidationError({
                'administered_date': 'Administered date is required for completed vaccinations.'
            })

        return attrs


class VaccinationListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing vaccinations.
    """
    pet_name = serializers.CharField(source='pet.name', read_only=True)

    class Meta:
        model = Vaccination
        fields = [
            'id',
            'pet',
            'pet_name',
            'vaccine_name',
            'due_date',
            'status',
            'administered_date',
        ]


class VaccinationDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for vaccination with pet information.
    """
    pet = PetListSerializer(read_only=True)
    veterinarian_name = serializers.CharField(
        source='veterinarian.get_full_name',
        read_only=True
    )
    veterinarian_email = serializers.EmailField(
        source='veterinarian.email',
        read_only=True
    )

    class Meta:
        model = Vaccination
        fields = [
            'id',
            'pet',
            'vaccine_name',
            'due_date',
            'status',
            'administered_date',
            'veterinarian',
            'veterinarian_name',
            'veterinarian_email',
            'batch_number',
            'notes',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'veterinarian_name', 'veterinarian_email']


class HealthRecordSerializer(serializers.ModelSerializer):
    """
    Serializer for HealthRecord model with full validation.
    """
    pet_name = serializers.CharField(source='pet.name', read_only=True)
    pet_id = serializers.IntegerField(source='pet.id', read_only=True)
    veterinarian_name = serializers.CharField(
        source='veterinarian.get_full_name',
        read_only=True
    )

    class Meta:
        model = HealthRecord
        fields = [
            'id',
            'pet',
            'pet_id',
            'pet_name',
            'weight',
            'notes',
            'record_date',
            'veterinarian',
            'veterinarian_name',
            'temperature',
            'heart_rate',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'pet_id', 'pet_name', 'veterinarian_name']

    def validate_weight(self, value):
        """
        Validate weight is positive.
        """
        if value <= 0:
            raise serializers.ValidationError('Weight must be greater than 0.')
        return value

    def validate_record_date(self, value):
        """
        Validate record date is not in the future.
        """
        if value > timezone.now().date():
            raise serializers.ValidationError('Record date cannot be in the future.')
        return value

    def validate_temperature(self, value):
        """
        Validate temperature is within reasonable range.
        """
        if value is not None:
            if value < 30.0 or value > 45.0:
                raise serializers.ValidationError(
                    'Temperature must be between 30°C and 45°C.'
                )
        return value

    def validate_heart_rate(self, value):
        """
        Validate heart rate is within reasonable range.
        """
        if value is not None:
            if value < 40 or value > 300:
                raise serializers.ValidationError(
                    'Heart rate must be between 40 and 300 bpm.'
                )
        return value

    def validate(self, attrs):
        """
        Cross-field validation.
        """
        return attrs


class HealthRecordListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing health records.
    """
    pet_name = serializers.CharField(source='pet.name', read_only=True)

    class Meta:
        model = HealthRecord
        fields = [
            'id',
            'pet',
            'pet_name',
            'weight',
            'record_date',
            'temperature',
            'heart_rate',
        ]


class HealthRecordDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for health record with pet information.
    """
    pet = PetListSerializer(read_only=True)
    veterinarian_name = serializers.CharField(
        source='veterinarian.get_full_name',
        read_only=True
    )
    veterinarian_email = serializers.EmailField(
        source='veterinarian.email',
        read_only=True
    )

    class Meta:
        model = HealthRecord
        fields = [
            'id',
            'pet',
            'weight',
            'notes',
            'record_date',
            'veterinarian',
            'veterinarian_name',
            'veterinarian_email',
            'temperature',
            'heart_rate',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'veterinarian_name', 'veterinarian_email']
